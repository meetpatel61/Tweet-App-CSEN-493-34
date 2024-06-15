#This file contains all the functions related to users like account creation, login, logout, geting user tweets and other profile info.

import sqlite3
from colorama import Fore
conn = sqlite3.connect('minitweet.db') #Establish connection to the database.
c = conn.cursor()
conn2 = sqlite3.connect('minitweet.db')
c2 = conn.cursor()

#Table for storing users info
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(80) NOT NULL PRIMARY KEY UNIQUE,
        password VARCHAR(80) NOT NULL, 
        followers INT DEFAULT 0,
        following INT DEFAULT 0,
        is_online BOOL DEFAULT 1
        );
""")

conn.commit()

#Function to check if username is already registered.
def registerCheck(username):
    try:
        givenUsers = c.execute("""
            SELECT * FROM users
            WHERE username = "{}"
        """.format(username))
        for user in givenUsers:
            return False
        return True
    except:
        return False

#Function to register a new user.    
def register(username, password):
    if not registerCheck(username):
        return False
    try:
        c.execute("""
            INSERT INTO users (username, password)
            VALUES ('{}', '{}');
        """.format(username, password))
        conn.commit()
        return True
    except:
        return False

#Function to check if username and password entered are valid.
def login(username, password):
    try:
        givenUsers = c.execute("""
        SELECT * FROM users
        WHERE username = "{}" AND password = "{}"
        """.format(username, password))
        for user in givenUsers:
            c.execute("""
                UPDATE users
                SET is_online = 1
                WHERE username = '{}'
            """.format(username))
            conn.commit()
            return True
        return False
    except:
        return False

#Function to logout a given user.
def logout(username):
    try:
        c.execute("""
                UPDATE users
                SET is_online = 0
                WHERE username = '{}'
            """.format(username))
        conn.commit()
        return True
    except:
        return False

#Function to parse the tweet body and return it in a formatted string. 
def parseTweetBody(body):
    res = body.split()
    lenb = len(res)
    for i in range(lenb):
        if res[i][0] in ['#', '@']:
            res[i] = Fore.CYAN + res[i] + Fore.WHITE
    return " ".join(res)

#Function to parse the tweet data and return it in a formatted string.
def parseTweet(tweetID, body, createdAt):
    res = Fore.CYAN + createdAt + Fore.WHITE + " - " + Fore.BLUE+ str(tweetID) + Fore.WHITE + "\n {} \n\n".format(parseTweetBody(body))
    return res

#Function to get the tweets which are pinned by the given username for his/her profile.
def getPinnedTweets(username):
    tweets = []
    try:
        pinnedTweets = c.execute(
            """
                SELECT tweets.tweetID, pins.username, tweets.body, tweets.createdAt
                FROM pins
                INNER JOIN tweets on pins.tweetID=tweets.tweetID
                WHERE pins.username = "{u}"
                ORDER BY id DESC
                LIMIT 5
            """.format(u = username))
        for data in pinnedTweets:
            tweets.append(parseTweet(data[0], data[2], data[3]))
        print(tweets)
        return tweets
    except:
        return tweets

#Function to get the profile data of the given username.        
def viewProfile(username):
    try:
        givenUsers = c.execute("""
            SELECT * FROM users
            WHERE username = "{}"
        """.format(username))
        doesExist = False
        currUser = None
        for user in givenUsers:
            doesExist = True
            currUser = user
        if not doesExist:
            return Fore.RED + "This username does not exist" + Fore.WHITE
        res = Fore.GREEN + username + Fore.WHITE + " - Followers : " + Fore.BLUE + str(currUser[2]) + Fore.WHITE + " Following : " + Fore.BLUE + str(currUser[3]) + Fore.WHITE + "\n" 
        pinnedTweets = getPinnedTweets(username)
        for tweets in pinnedTweets:
            res += tweets
        return res
    except:
        return Fore.RED + "Invalid Username" + Fore.WHITE

#Function to search for users matching the given pattern.
def search(pattern):
    try:
        givenUsers = c.execute("""
            SELECT username
            FROM users
            WHERE username LIKE "{}%"
            LIMIT 5
        """.format(pattern))
        res = ""
        for user in givenUsers:
            res += Fore.BLUE + " # "+  Fore.WHITE + user[0] + "\n"
        return Fore.BLUE + "Search results : \n" + Fore.WHITE + res
    except Exception:
        return Fore.RED + "Invalid search" + Fore.WHITE
