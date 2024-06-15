# In this file we derive data from command arguments and other database functions and then parse them. Once it is parsed, It finally executes the given commands.

from . import followersDb, groupsDb, tweetsDb, updatesDb, usersDb
from colorama import Fore
import socket
tokenCounter = 1
#An empty dictionary to map sessionID to username.
logData = {}
toSessionID = {}

#This function executes when a client establishes connection to the server's socket.
def init(data):
    global tokenCounter
    tokenCounter += 1
    return str(tokenCounter)

#Function to check the client's login status
def login(data):
    if len(data) != 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    username, password, sessionID = data
    if sessionID in logData:
        return Fore.BLUE + "User has already logged in" + Fore.WHITE
    if usersDb.login(username, password):
        logData[sessionID] = username
        toSessionID[username] = sessionID
        return Fore.GREEN + "Logged in successfully" + Fore.WHITE
    return Fore.RED + "Invalid Username/Password" + Fore.WHITE

#Function to check if a username has been already registered.
def register(data):
    if len(data) != 4:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    username, password, rePassword, sessionID = data
    if sessionID in logData:
        return Fore.BLUE + "User has already logged in" + Fore.WHITE
    elif password != rePassword:
        return Fore.RED + "Passwords don't match" + Fore.WHITE
    elif usersDb.register(username, password):
        logData[sessionID] = username
        toSessionID[username] = sessionID
        return Fore.GREEN + "Welcome to the Tweet App, " + Fore.GREEN + username + Fore.WHITE
    else:
        return Fore.RED + "User already exists" + Fore.WHITE

#Function to logout.
def logout(data):
    if len(data) != 1:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    sessionID = data[0]
    if sessionID not in logData:
        return Fore.RED + "No user is currently logged in" + Fore.WHITE
    else:
        if usersDb.logout(logData[sessionID]):
            toSessionID.pop(logData[sessionID])
            logData.pop(sessionID)
            return Fore.GREEN + "$Logged_out$" + Fore.WHITE
        else:
            return Fore.RED + "Cannot logout" + Fore.WHITE

#Function to add a certain user to the list of followers.
def addFollower(data):
    if len(data) != 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    followed, sessionID = data
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    follower = logData[sessionID]
    return followersDb.addFollower(follower, followed)

#Function to remove a certain follower from the list of followers.
def removeFollower(data):
    if len(data) != 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    followed, sessionID = data
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    follower = logData[sessionID]
    return followersDb.removeFollower(follower, followed)

#Function to retrieve a profile and view its profile stats like followers, following, tweets, etc.
def viewProfile(data):
    if len(data) != 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    username, sessionID = data
    return usersDb.viewProfile(username)

#Function to search for a username from the list of users.
def search(data):
    if len(data) != 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    pattern, sessionID = data
    return usersDb.search(pattern)

def postTweet(data):
    if len(data) < 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    sessionID = data[-1]
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE             
    username, body = logData[sessionID], " ".join(data[: -1])
    return tweetsDb.postTweet(username, body)

# Function to retrieve the most trending hashtags.
# def getTrending(data):
#     return tweetsDb.getTrending()

#Function to send private message to another user.
def sendMsg(data):
    if len(data) < 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    if data[-1] not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    sendTo, message, sessionID = data[0], " ".join(data[1:-1]) ,data[-1]
    isFollower = followersDb.isFollower(logData[sessionID], sendTo)
    if not isFollower:
        return Fore.RED + "You can only send a message to a follower" + Fore.WHITE
    if sendTo not in toSessionID:
        return Fore.GREEN +  "The user is currently not online. Try again later." + Fore.WHITE
    sendToPort = toSessionID[sendTo]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(sendToPort) + 1024))
    sock.send(bytes(Fore.CYAN + logData[sessionID] + Fore.WHITE + " :: {}".format(message), "utf-8"))
    sock.close()
    return Fore.GREEN + "Message sent." + Fore.WHITE

#get the updates for the given username
def getUpdates(data):
    if len(data) not in [1, 3]:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    sessionID = data[-1]
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    username = logData[sessionID]
    print(data, len(data))
    if len(data) == 3:
        if data[0] == "mark" and data[1] == "read":
            return updatesDb.markRead(username)
    return updatesDb.getUpdates(username)

#Function to broadcast messages in a created group.
def groupChat(data):
    sessionID = data[-1]
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    if len(data) < 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    username = logData[sessionID]
    groupname = data[0]
    msgBody = " ".join(data[1 : -1])
    membersList = groupsDb.getMembers(username, groupname, True)
    if not membersList:
        return Fore.RED + "You are not member of this group" + Fore.WHITE
    for targetUser in membersList:
        if targetUser not in toSessionID or targetUser == username:
            continue
        try:
            sendToPort = toSessionID[targetUser]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", int(sendToPort)+1024))
            sock.send(bytes("Group " + Fore.CYAN + groupname + Fore.WHITE + " - " + Fore.CYAN + username + Fore.WHITE + " " + msgBody, "utf-8"))
            sock.close()
        except:
            pass

#Function to create, delete, add, remove a group with members.
def group(data):
    sessionID = data[-1]
    if len(data) < 2:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    if sessionID not in logData: # put in server
        return Fore.RED + "Log in and try again" + Fore.WHITE
    if data[0] not in ["create", "add", "remove", "members", "delete"]:
        return Fore.RED + "Invalid command" + Fore.WHITE
    username = logData[sessionID]
    groupname = data[1]
    if data[0] == "create":
        return groupsDb.createGroup(username, groupname)
    elif data[0] == "add":
        return groupsDb.addMember(username, data[2:-1], groupname)
    elif data[0]=="remove":
        return groupsDb.removeMember(username, data[2:-1], groupname)
    elif data[0]=="members":
        members =  groupsDb.getMembers(username, groupname)
        if not members:
            return Fore.RED + "Does not have access to group members list" + Fore.WHITE
        return "Members - " + " ".join(members)
    elif data[0]=="delete":
        return groupsDb.removeGroup(username, groupname)

#Function to generate feed for the logged in user.
def getFeed(data):
    sessionID, numTweets, numPage = data[-1], 5, 1
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    username = logData[sessionID]
    if len(data) == 2:
        numTweets = int(data[0])
    elif len(data) == 3:
        numTweets, numPage = int(data[0]), int(data[1])
    elif len(data) > 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    tweets = tweetsDb.getFeed(username, numTweets, numPage)
    return "".join(tweets)

#Function to get tweets based on a given hashtag.
# def getHashtag(data):
#     numTweets, numPage = 5, 1
#     hashtag = data[0]
#     if len(data) == 3:
#         numTweets = int(data[1])
#     elif len(data) == 4:
#         numTweets, numPage = int(data[1]), int(data[2])
#     elif len(data) > 3:
#         return Fore.RED + "Invalid arguments" + Fore.WHITE
#     tweets = tweetsDb.getTweetsByTag(hashtag, numTweets, numPage)
#     return "".join(tweets)

#Function to get the tweets of currently logged in users.
def getPosts(data):
    numTweets, numPage = 5, 1
    if data[-1] not in logData:
        return "Log in and try again"
    username = logData[data[-1]]
    if len(data) == 2:
        numTweets = int(data[0])
    elif len(data) == 3:
        numTweets, numPage = int(data[0]), int(data[1])
    elif len(data) > 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    tweets = tweetsDb.getPosts(username, numTweets, numPage)
    return "".join(tweets)

#Function to pin a tweet to the profile.
def pinTweet(data):
    if data[-1] not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    username = logData[data[-1]]
    if len(data) == 2:
        tweetID = int(data[0])
    else:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    if tweetsDb.pinTweet(username, tweetID):
        return Fore.GREEN + "Pin successful" + Fore.WHITE
    return Fore.BLUE + "You have already pinned this tweet" + Fore.WHITE

def retweetID(data):
    if data[-1] not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    username = logData[data[-1]]
    if len(data) == 2:
        tweetID = int(data[0])
    else:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    return tweetsDb.retweetID(username, tweetID)

#Function to get list of all online followers.
def getOnline(data):
    sessionID, numFollowers, numPage = data[-1], 5, 1
    if sessionID not in logData:
        return Fore.RED + "Log in and try again" + Fore.WHITE
    username = logData[sessionID]
    if len(data) == 2:
        numFollowers = int(data[0])
    elif len(data) == 3:
        numFollowers, numPage = int(data[0]), int(data[1])
    elif len(data) > 3:
        return Fore.RED + "Invalid arguments" + Fore.WHITE
    onlineFollowers = []
    followers = followersDb.getOnline(username)
    for member in followers:
        if member in toSessionID:
            onlineFollowers.append(Fore.GREEN + "*" + Fore.WHITE + member)
    s, e  = (numPage - 1) * numFollowers, numPage * numFollowers
    return ("\n").join(onlineFollowers[s : e])
        
