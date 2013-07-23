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
CHANNEL = '#botbotclient'

# client name
USERNAME = 'botbotclient'
HOSTNAME = 'botbotclient'
SERVERNAME = 'botbotclient'
REALNAME = 'botbotclient'


#-------------------------------------------------------------------------------
#
# Client global variables
#
#-------------------------------------------------------------------------------

# debugging - You should keep this set to False when not debugging the bot.
#
# Setting this to True will make all socket reads and writes appear in the
# terminal. Setting this to False will disable most data displayed to the
# terminal but the bot will still log exceptions to the log file. Setting this
# is False also substantially increases the performance of the bot.
DEBUG = True

# logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs/log.log')


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
