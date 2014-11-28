### Twitter controlled TNT Cube builder ###
### Based on code by TeCoEd ###
### Working Version 4 ###
### Save into Pi/home folder###
 
import sys
import subprocess
import urllib
import time
import tweepy
import random
import ConfigParser
sys.path.append("../mcpi/api/python/mcpi")
import mcpi.minecraft as minecraft
import mcpi.block as block


def print_and_say(message):
    print message
    mc.postToChat(message)


def print_and_say_and_tweet(message, tweet=None):
    global send_tweet_messages
    message = time.strftime('%Y-%m-%d %H:%M:%S(UK) - ') + message
    print_and_say(message)
    if send_tweet_messages:
        if tweet is not None:
            api.update_status(message, tweet.id)
        else:
            api.update_status(message)


def say_blocks_left():
    global filledBlocks
    print_and_say_and_tweet("Blocks left: {}".format(len(filledBlocks)))


def place_block(tweet):
    global filledBlocks
    if filledBlocks:
        block_coord = filledBlocks.pop()
        mc.setBlock(block_coord["x"], block_coord["y"], block_coord["z"], block.TNT)
        print_and_say_and_tweet("Block placed at {}/{}/{} by @{}".format(block_coord["x"], block_coord["y"], block_coord["z"], tweet.user.screen_name), tweet)
        say_blocks_left()
    else:
        print_and_say_and_tweet("Sorry @{} - no more blocks left to place".format(tweet.user.screen_name), tweet)


print "Connecting to minecraft"
mc = minecraft.Minecraft.create()

mc.postToChat('Initialising')
print "Connected. Reading config"
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
access_token = config.get('Twitter','access_token')
access_token_secret = config.get('Twitter','access_token_secret')

twitter_username = config.get('Twitter','twitter_user_name')

send_tweet_messages_config = config.get('Twitter','send_tweet_messages')

send_tweet_messages = (send_tweet_messages_config == '1' or send_tweet_messages_config.lower() == 'true')

trigger_keyword=config.get('Options','keyword')
cubeSize = int(config.get('Options','block_size'))

print "Config complete. Connecting to Twitter"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print "Twitter authenticated"

totalBlocks = cubeSize * cubeSize * cubeSize

filledBlocks = []
blocksChecked = 0

mc.postToChat('Checking existing blocks')
print "Checking existing blocks"
for x in range(0, cubeSize):
    for y in range(0, cubeSize):
        for z in range(0, cubeSize):
            blockType = mc.getBlock(x,y,z)
            blocksChecked += 1
            if blockType != block.TNT.id:
                filledBlocks.append({"x":x,"y":y,"z":z})
                sys.stdout.write("Blocks checked: %d   \r" % (blocksChecked) )
                sys.stdout.flush()
            else:
                print "block at {}/{}/{} is TNT. Skipping".format(x,y,z)

mc.postToChat("{} existing TNT blocks found".format(totalBlocks-len(filledBlocks)))
print "{} existing TNT blocks found".format(totalBlocks-len(filledBlocks))
print "All blocks checked. Shuffling remaining spaces"
random.shuffle(filledBlocks)
say_blocks_left()


class BlockBuilder(tweepy.StreamListener):
    def on_status(self, tweet):
        if tweet.user.screen_name != twitter_username and trigger_keyword in tweet.text.lower():
            print ""
            print_and_say("@{}: {}".format(tweet.user.screen_name, tweet.text))
            place_block(tweet)
            time.sleep(5)


print "Initialising Twitter stream"
stream = tweepy.Stream(auth, BlockBuilder())
print_and_say_and_tweet("Listening for tweets. Tweet a message containing '{}' to @{}".format(trigger_keyword, twitter_username))

try:
    stream.userstream()
except KeyboardInterrupt:
    print "Exiting"
    stream.disconnect()
