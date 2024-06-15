#This file contains all functions related to followers.

import sqlite3
from colorama import Fore
conn = sqlite3.connect('minitweet.db')
c = conn.cursor()

#This creates the followers table.
c.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        follower VARCHAR(80) NOT NULL,
        followed VARCHAR(80) NOT NULL
        );
""")

conn.commit()

#This function adds a follower to the database
def addFollower(follower,followed):
    try:
        if(followed == follower):
            return Fore.RED + "Cannot follow yourself" + Fore.WHITE
        exist = c.execute("""
            SELECT username
            FROM users
            WHERE username = "{}"
        """.format(followed))
        doesExist = False
        for i in exist:
            doesExist = True
        if doesExist == False:
            return Fore.RED + "Invalid username" + Fore.WHITE
        already = c.execute("""
            SELECT *
            FROM followers
            WHERE follower = "{}" and followed = "{}"
        """.format(follower, followed))
        for i in already:
            return Fore.BLUE + "Already following" + Fore.WHITE
        follow(follower, followed)
        conn.commit()
        return Fore.GREEN + "Successfully started following " + Fore.BLUE + followed + Fore.WHITE
    except:
        return Fore.RED + "Unable to follow" + Fore.WHITE

#This function is used to add a follower to the database.
def follow(follower, followed):
    c.execute("""
            INSERT INTO followers VALUES ("{}", "{}")
        """.format(follower, followed))
    c.execute("""
            UPDATE users
            SET followers = followers + 1
            WHERE username = "{}";
        """.format(followed))
    conn.commit()
    c.execute("""
            UPDATE users
            SET following = following + 1
            WHERE username = "{}";
        """.format(follower))

#This function removes a follower from a specific user's follower list.
def removeFollower(follower, followed):
    try:
        already = c.execute("""
            SELECT *
            FROM followers
            WHERE follower = "{}" and followed = "{}"
        """.format(follower, followed))
        doesFollow = False
        for i in already:
            doesFollow = True
        if doesFollow != True:
            return Fore.RED + "Unable to unfollow" + Fore.WHITE
        c.execute("""
            DELETE FROM followers
            WHERE follower = "{}" and followed = "{}"
        """.format(follower, followed))
        conn.commit()
        c.execute("""
            UPDATE users
            SET followers = followers - 1
            WHERE username = "{}";
        """.format(followed))
        conn.commit()
        c.execute("""
            UPDATE users
            SET following = following - 1
            WHERE username = "{}";
        """.format(follower))
        conn.commit()
        return Fore.GREEN + "Successfully unfollowed "+ Fore.BLUE + followed + Fore.WHITE
    except:
        return Fore.RED + "Unable to unfollow" + Fore.WHITE

#This function getes the list of followers (both online and offline) for the given username (this is used as a utility function to check which followers are online)
def getOnline(username):
    followersList = []
    try:
        dataRows = c.execute("""
            SELECT follower
            FROM followers 
            where followed = '{u}'
        """.format(u = username))
        for data in dataRows:
            followersList.append(data[0])
        return followersList
    except:
        return followersList

#This function returns True or False if 'username' is follower of a user.
def isFollower(username, targetUser):
    try:
        dataRows = c.execute("""
            SELECT follower
            FROM followers 
            where followed = '{u}' AND follower = '{t}'
        """.format(u = username, t = targetUser))
        for data in dataRows:
            return True
        return False
    except:
        return False