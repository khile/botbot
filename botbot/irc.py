"""IRC event handlers"""

def pong(r, line, bot, chan):
    """Send a pong in response to a ping"""
    host = r.group(1)
    bot.write('PONG :{}\r\n'.format(host))

def netsplit(r, line, bot, chan):
    """Raise an exception on netsplit so the mainloop will catch it and restart
    the client

    """
    raise Exception('Netsplit exception')

def error(r, line, bot, chan):
    """Raise an exception on IRCD error so the mainloop will restart the
    client

    """
    raise Exception('IRCD Error "{}"'.format(line))
