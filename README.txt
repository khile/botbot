
                           _.:` botbot `:._

  This is a Python 3 IRC client which uses multiprocessing. It comes with some
basic builtin IRC utility functions, but really excels in giving the user easy
extensibility of the bots functionality.

  To run the bot just modify the values in conf.py and run botbot.py.

  The client defaults to running in debug mode but you can disable it in the
configuration file (conf.py).

  Functionality can be added or modified by editing definitions.py. Here you
have a dictionary for each type of parser you want to run. This structure
associates a name with a tuple consisting of a regular expression, and a
function pointer. When the client starts it associates each one of the
dictionaries with a parser. After the client connects to the IRC server the
client loops through all messages from the server and sends them off to a
parser. The parser then checks the data against all of its regular expressions.
When a match appears the corresponding function is called. This is where the
user can add functionality.

  Currently there is a set of definitions for the IRC protocol messages, and
another for custom utility functions. If you don't want to create another type
and/or parser, then you can just add definitions to definition.py inside the
CUST_DEFINITIONS deictionary, and then you would define the corresponding
funtions in custom.py. Looking over the given utility functions in
definitions.py and custom.py should give you a clear picture of how to extend
functionality.


Source description:
    bobot.py - IRC client
    botbot/
        bangs.py - DuckDuckGo search bangs
        bot.py - Socket I/O abstraction
        conf.py - Global variables
        custom.py - Custom event handlers
        debug.py - Interface I/O functions
        definitions.py - Event mappings
        irc.py - IRC event handlers
        parser.py - Parses messages for events
        data/
            data.sqlite - Database used by custom.py
            help.txt - help manual
            lstell.txt - lstell manual
            q.txt - q manual
            tell.txt - tell manual
            urlq.txt - urlq manual
            urls.txt - urls manual
        logs/
            log.log - Client log file
