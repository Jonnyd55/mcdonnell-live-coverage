Live Coverage of McDonnell Trial
=========

This is the stack I used to push live updates to the home page of [PilotOnline.com][1] during the corruption trial of former Virginia governor Bob McDonnell.

<img src="http://jondavenport.com/wp-content/uploads/2014/09/mcdonnell.jpg">

The Updates
---
__The files:__

1. trial.py



The updates came from two place: a twitter feed (or list of twitter users) and a [CoveritLive][2] event. 

I used [Requests][3] and the [CoveritLive API][4] to pull newsflashes from the event, which is where the rest of our coverage was being hosted. I also used [python-twittery][5] to do the twitter data processing.

The script was designed to be started up by online producers who wouldn't need to touch the code, though various aspects of it needed to change (like the CoverItLive event ID and the Twitter users). They just needed to answer a series of prompts in the command line once the script fired. Once it is fired, the prompts look like this:

    C:\projects\mcdonnell>python trial.py
    Enter the altcast code: [[Code here]]
    Enter the number of twitter users: 1
    Enter the twitter handle of the user: kathymarievb
    Firing updates, starting at Wed Sep 10 17:27:02 2014
    ________________
    Updating JSON with the following info:
    



The widget
---
__The files:__

1. ajax.html

2. script.js

3. tweets.json

4. updates.json

5. styles.css

I fire Ajax requests at my server to pull the JSON objects down and fill up my widget. I also set a timer so the widget will update automatically every five minutes without having to refresh the page, so if you leave the tab open, you would have the latest updates when you come back.

I used [handlebars][6] to handle the templating. 


License
----

MIT


[1]:http://pilotonline.com
[2]:http://www.coveritlive.com/
[3]:http://docs.python-requests.org/en/latest/
[4]:http://www.coveritlive.com/index.php?option=com_content&task=view&id=280
[5]:https://github.com/bear/python-twitter
[6]:http://handlebarsjs.com/
