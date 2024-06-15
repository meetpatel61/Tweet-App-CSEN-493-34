# This file contains commands that user enters. We map those commands to the respective function(located in the file views.py) that we want to run. 

from . import views

functions = {
    "init": views.init,                 # initialize the client
    "login": views.login,               # login {username}. logs in the existing user
    "register": views.register,         # register {username}. registers a new user
    "logout": views.logout,             # logout. logs out the logged-in user
    "follow": views.addFollower,        # follow {username}. user can follow another user
    "unfollow": views.removeFollower,   # unfollow {username}. user can unfollow an existing follower
    "profile": views.viewProfile,       # profile {username}. user can see the follower and following count
    "search": views.search,             # search {username}. user can search for other registered users
    "tweet": views.postTweet,           # tweet {message} (optional). user can tweet messages. user can also just enter tweet to type a long tweet 
    # "trending": views.getTrending,      # 
    "msg": views.sendMsg,               # msg {username} {message} user can send a message to another user provided the user is in the following list
    "updates": views.getUpdates,        # updates. see if anyone mentions you in a tweet or retweets your tweet.
    "group": views.group,               # group {create, add, remove, members, delete} 
                                        # group create {groupname} user can create a group and will be the owner of the group.
                                        # group add {groupname} {username} the user(owner) can add members to the group.
                                        # group remove {groupname} {username} the user(owner) can remove members to the group.
                                        # group members {groupname} the user can see who are the members of the group
                                        # group delete {groupname} the user(owner) can delete the group
    "stream": views.groupChat,          # stream {groupname} {message}. members of the group can send messages to all the other members in the group.
    "feed": views.getFeed,              # feed. user can check the tweets and retweets of the users in the following list
    # "hashtag": views.getHashtag,        # 
    "posts": views.getPosts,            # posts. user can check their own tweets and retweets
    "pin": views.pinTweet,              # pin {tweetID}. user can pin a tweet so that the tweet is visible on the user's profile  
    "retweet": views.retweetID,         # retweet {tweetID}. user can retweet a tweet from the tweetID.
    "online": views.getOnline           # online. user can see other currently online users from his following list.
}