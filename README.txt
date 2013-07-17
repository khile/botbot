
                          botbot

  This is a Python 3 light IRC client which uses multiprocessing for concurrent processing. It comes with some basic builtin IRC utility functions, but really excels in giving the user easy extensibility of the bots functionality.
  
  To run the bot just modify the values in conf.py and run irclient.py.
  
  The client defaults to running in debug mode but you can disable it the connect funtion in irclient.py. Change "B = Bot(host, int(port), debug=True)" to "B = Bot(host, int(port), debug=False)". Errors will still be written to logs/log.log.
  
  Functionality can be added or modifying by editing definitions.py. Here you have a dictionary for each type of parser you want to run. This structure associates a name with a tuple consisting of a regular expression, and a function pointer. When the client starts it associates each one of the dictionaries with a parser. After the client connects to the IRC server the client loops through all messages from the server and send them off to a parser. The parser then checks the data against all of it's regular expressions. When a match appears the corresponding function is called. This is where the user can add functionality. Currently there is a set of definitions for the IRC protocol messages, and another for custom utility functions. If you don't want to create another type and/or parser, then you can just add definitions to definition.py inside the CUST_DEFINITIONS deictionary, and then you would define the corresponding funtions in custom.py. Looking over the given utility functions in custom.py and irclient.py should give you a clear picture of how to extend functionality.