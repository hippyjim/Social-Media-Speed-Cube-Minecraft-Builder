Social-Media-Speed-Cube-Minecraft-Builder
=========================================

Send a Tweet, builds a block in Minecraft (10 x 10 x 10)

Full details and example video here: http://www.tecoed.co.uk/speed-cube.html

To use:

Install the Twitter-Block.py script in a suitable folder. Copy the config-sample.txt into the same folder,
renaming it to config.txt. Fill in your Twitter details in the config.txt file.

Make sure your Minecraft server is running, then start the Twitter-Block.py script. 

The script will check the area in the centre of your minecraft world and count the number of TNT blocks already 
in place, and adjust the block count accordingly. 

Once the script is running it will print "About to listen" to the console. Depending on your version of Tweepy
you may see an error message like "ERROR:root:Unknown message type: {"friends":[]}". This is safe to ignore.

When the script has set up and is listening, send a tweet to your Twitter account containing the word "block" - e.g.
 
@MyTwitter Build a block

 or
 
@MyTwitter block.

The script will place a block in one of the empty spaces and say in chat how many blocks are left. 

Once all blocks are in place the script will give a different message.
