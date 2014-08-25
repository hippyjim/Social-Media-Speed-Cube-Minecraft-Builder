###TeCoEd ###
###wORKING vERSION 3###
### Save into Pi/home folder###
 
import sys, subprocess, urllib, time, tweepy, random, ConfigParser
# sys.path.append("./mcpi/api/python/mcpi")
import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()

config = ConfigParser.RawConfigParser()
config.readfp(open(r'config.txt'))
# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key= config.get('Twitter','consumer_key')
consumer_secret= config.get('Twitter','consumer_secret')

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token=  config.get('Twitter','access_token')
access_token_secret=  config.get('Twitter','access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

###twitter block builder###
Blocks_Left = 1000

def build_blocks():
    block = 46,1
    x = random.randint(0, 5) ### 5 x 5 x 5 
    y = random.randint(0, 5)
    z = random.randint(0, 5)

    ###TEST THE TWITTER INTERACTION place a single block###
    #pos = mc.player.getPos()###testing tweets work
    #x = pos.x
    #y = pos.y
    #z = pos.z
    
    mc.setBlock(x, y, z, block)
    print "Block Placed"

  
class BlockBuilder(tweepy.StreamListener):
    def on_status(self, tweet):
        global Blocks_Left
        #if tweet.text == "@JimPiri block":
        if "block" in tweet.text:
            build_blocks()
            print tweet.text
            print ""
            print tweet.user.screen_name + " placed a block!"
            mc.postToChat(tweet.user.screen_name)
            mc.postToChat("placed a block")
            Blocks_Left = Blocks_Left - 1 
            print ""
            print "Blocks left to build =", Blocks_Left
            mc.postToChat("Blocks left to place")
            mc.postToChat(Blocks_Left)
            time.sleep(5)
                   
        else:
            print tweet.text
            print tweet.user.screen_name
            print""
            time.sleep(5)

print "Initialising"
stream = tweepy.Stream(auth, BlockBuilder())
print "About to listen"

try:
    stream.userstream()
except KeyboardInterrupt:
    print "Exiting!"
    stream.disconnect()
