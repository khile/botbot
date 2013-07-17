"""Custom event handlers"""
import gzip
import html.parser
import io
import os
import re
import socket
import sqlite3
import time
import traceback
import urllib.request

from bangs import BANG_DICT
from conf import (DB_FILE,
                  HELP_FILE,
                  URL_SEARCH_LIMIT,
                  USER_AGENT)
from debug import debug


def list_help(r, line, bot, chan):
    """List the custom commands via PM"""
    param = None
    try:
        param = r.group(6)
    except KeyError:
        pass
    if param:
        if param[0] == '!':
            name = param[1:]
        else:
            name = param
    else:
        name = 'help'
    nick = r.group(1)
    try:
        f = open(HELP_FILE.format(name=name), 'r')
    except IOError:
        bot.write('PRIVMSG {nick} :{param} does not exist.\r\n'.format(
                    nick=nick, param=param))
        return
    for l in f.readlines():
        l = l.rstrip()
        if not l:
            bot.write('PRIVMSG {nick} : \r\n'.format(nick=nick))
        else:
            bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=l))
    f.close()

def title_echo(r, line, bot, chan):
    """Echo the title of a url via MC"""
    def write_url(title, url):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        t = (title, url)
        c.execute('INSERT INTO url_history VALUES (?, ?)', t)
        conn.commit()
        conn.close()
    url = r.group(5).split()[0]
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]
    try:
        f = opener.open(url)
        html = f.read(1048576) # only read the first 2**20 bytes
    except:
        e = traceback.format_exc()
        debug(e, log_only=True)
        write_url(None, url)
        return
    try:
        encoding = f.info()['content-encoding']
    except KeyError:
        encoding = None
    if encoding and encoding == 'gzip':
        html = io.BytesIO(html)
        gz = gzip.GzipFile(fileobj=html, mode='rb')
        html = gz.read()
        gz.close
    f.close()
    html = html.decode('utf-8', errors='replace')
    title = re.search(
                r'<title.*?>(.*?)</title>',
                html,
                re.DOTALL | re.IGNORECASE)
    if title:
        title = title.group(1).strip()
        title = title.replace('\n', '').replace('\r', '')
        title = ' '.join([w for w in title.split(' ') if w != ''])
        title = html.parser.HTMLParser().unescape(title)
    else:
        write_url(None, url)
        return
    bot.write('PRIVMSG {chan} :Title: {msg}\r\n'.format(chan=chan, msg=title))
    write_url(title, url)

def tell(r, line, bot, chan):
    """Add a tell to the database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    sender = r.group(1)
    to = r.group(5)
    msg = r.group(6)
    now = time.strftime('%b-%d::%H:%M', time.localtime())
    complete_msg = '{to}: {time} <{sender}> {msg}'.format(
                    to=to, time=now, sender=sender, msg=msg)
    to = to.lower()
    t = (to, complete_msg)
    c.execute('''INSERT INTO tells VALUES (?, ?)''', t)
    conn.commit()
    conn.close()

def echo_tell(r, line, bot, chan):
    """When the user joins the channel echo their tells via MC"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    nick = r.group(1).lower()
    t = (nick,)
    c.execute('''SELECT message
                 FROM tells
                 WHERE nick=?''', t)
    tells = c.fetchall()
    for message in tells:
        bot.write('PRIVMSG {chan} :{msg}\r\n'.format(chan=chan, msg=message[0]))
    c.execute('''DELETE FROM tells
                 WHERE nick=?''', t)
    conn.commit()
    conn.close()

def list_tell(r, line, bot, chan):
    """List pending tells via PM or MC"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT message
                 FROM tells
                 ORDER BY nick''')
    tells = c.fetchall()
    tells = [t for t in tells]
    nick = r.group(1)
    reply_main = r.group(4)[0] == '#'
    if reply_main:
        bot.write('PRIVMSG {chan} :{msg}\r\n'.format(chan=chan, msg=str(tells)))
    else:
        bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=str(tells)))

def echo_urls(r, line, bot, chan):
    """Echo url rows from database via PM"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT title, url
                 FROM url_history''')
    urls = c.fetchall()
    conn.close()
    nick = r.group(1)
    count = r.group(6)
    if count is None:
        count = 5
    count = int(count) if int(count) < URL_SEARCH_LIMIT else URL_SEARCH_LIMIT
    for i in range(1, count + 1):
        if len(urls) - i < 0:
            break
        url = urls[i * -1]
        msg = '{i}. {title}'.format(i=i, title=url[0])
        bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=msg))
        msg = '    {url}'.format(url=url[1])
        bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=msg))

def url_search(r, line, bot, chan):
    """Search the database for a row which contains the search query via PM"""
    nick = r.group(1)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    queries = r.group(5).strip().split()
    row_set = set()
    for query in queries:
        query = '%' + query + '%'
        t = (query, query)
        c.execute('''SELECT title, url
                     FROM url_history
                     WHERE title LIKE ? OR url LIKE ?''', t)
        row_set |= set(c.fetchall())
    conn.close()
    urls = tuple(row_set)[:URL_SEARCH_LIMIT]
    for i in range(len(urls)):
        url = urls[i]
        msg = '{i}. {title}'.format(i=i + 1, title=url[0])
        bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=msg))
        msg = '    {url}'.format(url=url[1])
        bot.write('PRIVMSG {nick} :{msg}\r\n'.format(nick=nick, msg=msg))

def query_engine(r, line, bot, chan):
    """Echo a duck duck go search results link"""
    query = r.group(5).strip()
    bang = re.search(r'(!\w+)', query, re.IGNORECASE)
    if bang and bang.group(1) in BANG_DICT:
        bot.write('PRIVMSG {chan} :Search {name} for "{query}":\r\n'.format(
                    chan=chan,
                    name=BANG_DICT[bang.group(1)],
                    query=query.replace(bang.group(1), '').strip()
                 ))
    else:
        bot.write('PRIVMSG {chan} :Search for "{query}":\r\n'.format(
                    chan=chan,
                    query=query
                 ))
    query = query.replace(' ', '%20')
    bot.write('PRIVMSG {chan} :https://duckduckgo.com/?q={msg}\r\n'.format(
                chan=chan,
                msg=query
             ))
