======================================================================================
``display-session``: Convenient formatting, coloring and utility for print statements.
======================================================================================

**display-session** is an MIT licensed Python package that provides easy ANSI formatting and utility to Python's built in print statement.

This project stemmed from wanting better looking, more informative, and more engaging command line interfaces.

There are three functions intended to be user-facing:

1. header - print provided message with all other space as the provided justify_char. Serves as easy way to communicate seperate sections within logs.

2. alert - simple print statement that maps numeric arg (-1, 0, 1) to bad, neutral, good. Serves as easy way to communicate sentiment of message.

3. report - most complicated print statement. proceeds all messages with bylines, and if provided will run all provided functions at print time. intended to serve as a sort of heads-up-display for the command line. See example below.

Simple comparison and examples::
    
    >>>print('This is how the builtin print function works')
    This is how the builtin print function works


Simplest compelling usecase for display_session::

    >>>from display_session import DisplaySession
    >>>display = DisplaySession('This is a byline') 
    >>>display.report('The byline proceeds any text input here')
    
    # hard to show with markdown, but byline is also separately ANSI colored.
    This is a byline  : The byline proceeds any text input here
    
    
More complicated examples::
    
    >>>import datetime as dt
    >>>import psutil
    
    >>>from display_session import DisplaySession
    >>>user = 'John'
    
    >>>display = DisplaySession(byline='P R O G R A M - {}'.format(user), 
                                byline_action=[dt.datetime.now, psutil.cpu_percent]
                                )
    >>>display.report('User successfully logged in')
     P R O G R A M - John  // 2018-09-19 21:55:29.115387 // 9.1: User successfully logged in.
    >>>display.report('User successfully logged out')
     P R O G R A M - John  // 2018-09-19 21:56:14.560489 // 7.8: User successfully logged out.
     
Other capabilities::
     
    >>># lets signify to our users that we are entering a new section
    >>>display.header('BEGINNING LEVEL 2', align='right')
    ______________________________________________________________________ BEGINNING LEVEL 2

    >>># lets communicate by leveraging ANSI colors - our second arg maps to them in the method.
    >>>display.alert('This message is good, so it should have a green color', 1)
    This message is good, so it should have a green color
    >>>
    >>>display.alert('This message is bad, so it should have a red color', -1)
    This message is bad, so it should have a red color

