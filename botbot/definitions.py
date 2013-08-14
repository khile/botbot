"""Definitions for parsing lines"""
from botbot.custom import (echo_tell,
                           echo_urls,
                           list_help,
                           list_tell,
                           tell,
                           title_echo,
                           url_search,
                           query_engine)
from botbot.irc import error, pong, netsplit


CUST_DEFINITIONS = {
    'echo_tell': (
        r'^:(.+)!~?(.+)@(.+)\sJOIN\s(.+)$',
        echo_tell
    ),
    'echo_urls': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!urls(\s(\d+))?$',
        echo_urls
    ),
    'list_help': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!help(\s(!?\w+))?$',
        list_help
    ),
    'list_tell': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!lstell$',
        list_tell
    ),
    'tell': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!tell\s([\w-]+)\s(.+)$',
        tell
    ),
    'title_echo': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:.*(https?://.+)$',
        title_echo
    ),
    'url_search': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!urlq\s(.+)$',
        url_search
    ),
    'query': (
        r'^:(.+)!~?(.+)@(.+)\sPRIVMSG\s(.+)\s:!q\s(.+)$',
        query_engine
    ),
}

IRC_DEFINITIONS = {
    'error': (
        r'^ERROR\s:(.*)$',
        error
    ),
    'pong': (
        r'^PING\s:(.*)$',
        pong
    ),
}
