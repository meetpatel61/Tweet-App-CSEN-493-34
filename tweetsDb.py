#This file contains all functions related to tweets like posting, retweeting, geting, pinning etc.

import sqlite3
from colorama import Fore
conn = sqlite3.connect('minitweet.db')
c = conn.cursor()

#This table stores all the tweets.
conn.commit()
c.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        tweetID INTEGER PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        body VARCHAR(300) NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
        );
""")

conn.commit()

#This table stores all the hashtags for tweetIDs
c.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY,
        tag VARCHAR(80) NOT NULL,
        tweetID INTEGER NOT NULL,
        FOREIGN KEY (tweetID) REFERENCES tweets(tweetID)
    );
""")

#This table stores all the pinned tweets for usernames
c.execute("""
    CREATE TABLE IF NOT EXISTS pins (
        id INTEGER PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        tweetID INTEGER NOT NULL,
        FOREIGN KEY (tweetID) REFERENCES tweets(tweetID)
    );
""")
conn.commit()

#This function getes all the tweets for a given hashtag.
def getHastags(body):
    body = body.split()
    tags = []
    for word in body:
        if (word[0] == '#'):
            tags.append(word[1: ])
    return tags

#This function checks if a user exists in the database or not.
def doesUserExist(username):
    try:
        givenUsers = c.execute("""
            SELECT * FROM users
            WHERE username = "{}"
        """.format(username))
        for user in givenUsers:
            return True
        return False
    except:
        return False

#This function posts an update to the user if he is mentioned in a tweet.
def postMentionUpdate(fromUser, targetUser, tweetID):
    body = fromUser + " mentioned you in his tweetID : " + str(tweetID) + "."
    try:
        c.execute("""
            INSERT INTO updates (username, body)
            VALUES ('{}', '{}')
        """.format(targetUser, body))
        conn.commit()
    except:
        pass

#This function posts an update to the user if his tweet has been retweeted by another user.
def postRetweetUpdate(fromUser, targetUser, tweetID):
    try:
        body = fromUser + " retweeted your tweet " + str(tweetID) + ". "
        c.execute("""
                INSERT INTO updates (username, body)
                VALUES ('{}', '{}')
            """.format(targetUser, body))
        conn.commit()
    except:
        pass

#This function parses the message body and returns a list of all users mentioned in the tweet.
def getMentions(username, body, tweetID):
    body = body.split()
    mentions = []
    for word in body:
        if (word[0] == '@'):
            if doesUserExist(word[1:]):
                mentions.append(word[1: ])
    for mention in mentions:
        postMentionUpdate(username, mention, tweetID)
    
#This function posts a tweet by a given username and tweet body.
def postTweet(username, body):
    try:
        if not body:
            return "The body does not exists."
        c.execute("""
            INSERT INTO tweets (username, body)
            VALUES ('{}', '{}')
        """.format(username, body))
        conn.commit()
        postIDCursor = c.execute("""
            SELECT last_insert_rowid();
        """)
        tweetID = postIDCursor.fetchone()[0]
        hashtags = getHastags(body)
        for tag in hashtags:
            c.execute("INSERT INTO tags (tag, tweetID) VALUES (?, ?)", (tag, tweetID))
            conn.commit()
        getMentions(username, body, tweetID)
        return Fore.GREEN + "Successfully posted" + Fore.WHITE 
    except:
        return Fore.RED + "Tweet cannot be posted. Try again later." + Fore.WHITE

#This function gets the topmost trending hashtags.
# def getTrending():
#     try:
#         trends = c.execute("""
#             SELECT tags.tag, COUNT(*)
#             FROM tags
#             INNER JOIN tweets ON tags.tweetID=tweets.tweetID
#             WHERE tweets.created_at >= datetime('now','-1 day')
#             GROUP BY tags.tag
#             ORDER BY 2 DESC
#             LIMIT 5;
#         """)
#         res = ""
#         rank = 1
#         for trend in trends:
#             res = res + (Fore.BLUE + "#" + str(rank) + Fore.WHITE + " " + trend[0] + " - " + str(trend[1]) + "\n")
#             rank += 1
#         return res
#     except:
#         return Fore.RED + "Cannot get trending hashtags." + Fore.WHITE

#This function gets the following list
def getFollowing(username):
    followingList = []
    try:
        followings = c.execute("""
            SELECT followed from followers
            WHERE follower = ?
        """, (username,))
        for following in followings:
            followingList.append(following[0])
        return followingList
    except:
        return followingList

#This function parses the tweet body for hashtags and mentions.
def parseTweetBody(body):
    res = body.split()
    lenb = len(res)
    for i in range(lenb):
        if res[i][0] in ['#', '@']:
            res[i] = Fore.CYAN + res[i] + Fore.WHITE
    return " ".join(res)

def parseTweet(tweetID, username, body, createdAt):
    res =  Fore.MAGENTA + username + Fore.WHITE + " : " + Fore.CYAN + createdAt + Fore.WHITE + " - " + Fore.BLUE + str(tweetID) + Fore.WHITE+ "\n" + parseTweetBody(body) + "\n\n"
    return res

#This function getes the tweet feed for a given username.
def getFeed(username, numTweets = 5, offsetPage = 1):
    tweets = []
    try:
        followingList = getFollowing(username)
        if not followingList:
            return []
        queryText = "( '" + followingList[0] + "' "
        followingList = followingList[1:]
        for member in followingList:
            queryText += ", '" + member + "' "
        queryText += ")"
        dataRows = c.execute("""
            SELECT * from tweets
            WHERE username IN {a}
            ORDER BY created_at DESC
            LIMIT {c}
            OFFSET {b}
        """.format(a = queryText, c = numTweets, b = numTweets * (offsetPage - 1)))
        for data in dataRows:
            tweets.append(parseTweet(data[0], data[1], data[2], data[3]))
        return tweets
    except:
        return tweets

#This function getes the tweets for a given hashtag.
# def getTweetsByTag(hashtag, numTweets = 5, numPage = 1):
#     tweets = []
#     try:
#         dataRows = c.execute("""
#             SELECT * from tweets
#             INNER JOIN tags ON tags.tweetID=tweets.tweetID
#             WHERE tags.tag = '{t}'
#             LIMIT {l}
#             OFFSET {o}
#         """.format(t = hashtag, l = numTweets, o = numTweets * (numPage - 1)))
#         for data in dataRows:
#             tweets.append(parseTweet(data[0], data[1], data[2], data[3]))
#         return tweets
#     except:
#         return tweets

#This function getes the tweets for a given username.
def getPosts(username, numTweets = 5, numPage = 1):
    tweets = []
    try:
        dataRows = c.execute("""
            SELECT * from tweets
            WHERE username = '{u}'
            ORDER BY created_at DESC
            LIMIT {l}
            OFFSET {o}
        """.format(u = username, l = numTweets, o = numTweets * (numPage - 1)))
        for data in dataRows:
            tweets.append(parseTweet(data[0], data[1], data[2], data[3]))
        return tweets
    except:
        return tweets

#This function pins the tweets for a given username.
def pinTweet(username, tweetID):
    try:
        pinnedRows = c.execute("""
        SELECT * from pins 
        WHERE username = '{u}' AND tweetID = {t}
        """.format(u = username,t = tweetID))
        for row in pinnedRows:
            return False
        c.execute("""
        INSERT INTO pins (username, tweetID)
        VALUES ('{u}', {t})
        """.format(u = username, t = tweetID))
        conn.commit()
        return True
    except:
        return False

#This function retweets a given tweet for a given username.
def retweetID(username, tweetID):
    try:
        foundTweets = c.execute("""
            SELECT * from tweets
            WHERE tweetID = {t}
        """.format(t = tweetID))
        tweetBody = ""
        for tweet in foundTweets:
            targetUser = tweet[1]
            tweetBody = "Retweeted username: {u} tweetID : {t}\n".format(u = targetUser, t = tweetID)
            tweetBody += tweet[2]
            postTweet(username, tweetBody)
            postRetweetUpdate(username, targetUser, tweetID)
            return Fore.GREEN + "Retweet successful" + Fore.WHITE
        return Fore.RED + "Cannot retweet" + Fore.WHITE
    except:
        return Fore.RED + "Cannot retweet" + Fore.WHITE