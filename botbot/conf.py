"""This is where all global data can be altered"""
import os
import random
import string


#-------------------------------------------------------------------------------
#
# IRC protocol values
#
#-------------------------------------------------------------------------------

# timing
RETRY_INTERVAL = 5 # seconds
PING_INTERVAL = 30 # seconds

# server
SERVER = 'irc.freenode.net'
PORT = 6667
CHANNEL = '#bottbotclient'

# client name
USERNAME = 'botbotclient'
HOSTNAME = 'botbotclient'
SERVERNAME = 'botbotclient'
REALNAME = 'botbotclient'


#-------------------------------------------------------------------------------
#
# custom.py global variables
#
#-------------------------------------------------------------------------------

# file paths
DB_FILE = os.path.join(os.path.dirname(__file__), 'data/data.sqlite')
HELP_FILE = os.path.join(os.path.dirname(__file__), 'data/{name}.txt')

# urllib title echo user agent
_myrg = random.SystemRandom()
_length = 20
_alphabet = string.ascii_letters[0:52] + string.digits
USER_AGENT = str().join(_myrg.choice(_alphabet) for _ in range(_length))

# URL results limit
URL_SEARCH_LIMIT = 25
