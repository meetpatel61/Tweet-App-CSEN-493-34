#This file contains all the functions relaated to the groups like creation, deletion, adding annd removing users.

import sqlite3
conn = sqlite3.connect('minitweet.db')
c = conn.cursor()
conn2 = sqlite3.connect('minitweet.db')
c2 = conn2.cursor()

#This table holds the group data.
c.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        groupname VARCHAR(80) NOT NULL PRIMARY KEY UNIQUE,
        username VARCHAR(80) NOT NULL,
        members INT DEFAULT 0
        );
""")

conn.commit()

#This table is used to store group members.
c.execute("""
    CREATE TABLE IF NOT EXISTS groupmembers (
        group_id INTEGER PRIMARY KEY,
        groupname VARCHAR(80) NOT NULL,
        username VARCHAR(80) NOT NULL
        );
""")

conn.commit()

#This function checks if a user exists in the given group.
def doesUserExist(username):
    try:
        givenUsers = c2.execute("""
            SELECT * FROM users
            WHERE username = "{}"
        """.format(username))
        for user in givenUsers:
            return True
        return False
    except:
        return False

#This function checks if a group exists.
def doesGroupExist(groupname):
    try:
        givenGroups = c2.execute("""
            SELECT * FROM groups
            WHERE groupname = "{}"
        """.format(groupname))
        for group in givenGroups:
            return True
        return False
    except:
        return True

#This function checks if the username is the owner of the group.
def isGroupOwner(username, groupname):
    try:
        givenRows = c2.execute("""
            SELECT * FROM groups
            WHERE groupname = "{}" AND username = "{}"
        """.format(groupname, username))
        for row in givenRows:
            return True
        return False
    except:
        return False

#This function checks if the username is a member of the group.
def doesMemberExist(username, groupname):
    try:
        givenRows = c.execute("""
            SELECT * FROM groupmembers
            WHERE groupname = "{}" AND username = "{}"
        """.format(groupname, username))
        for i in givenRows:
            return True
        return False
    except:
        return False

#This function checks if the groupname exists or not and if it does not then a new group is created.
def createGroup(username, groupname):
    try:
        if doesGroupExist(groupname):
            return "Group name is already in use. Try another name."
        c.execute("""
            INSERT INTO groups (groupname, username)
            VALUES ('{}', '{}')
        """.format(groupname, username))
        conn.commit()
        usernames = [username] #Group Owner Added
        addMember(username, usernames, groupname)
        return "Group created"
    except:
        return "Unable to create the group"

#This function adds member to the group.
def addMember(username, addNames, groupname):
    if not isGroupOwner(username, groupname):
        return "You are not the owner of the group, contact group admin"
    added = []
    try:
        for user in addNames:
            if doesUserExist(user) and not doesMemberExist(user, groupname):
                c.execute("""
                    INSERT INTO groupmembers (groupname, username)
                    VALUES ('{}', '{}')
                """.format(groupname, user))
                conn.commit()
                c.execute("""
                    UPDATE groups
                    SET members = members + 1
                    WHERE groupname = "{}";
                """.format(groupname))
                conn.commit()
                added.append(user)
    except:
        pass
    finally:
        return " ".join(added) + " added in " + groupname

#This function removes the member from the group.
def removeMember(username, removeNames, groupname):
    if not isGroupOwner(username, groupname):
        return "Only owner of the group can remove members."
    deleted = []
    try:
        for user in removeNames:
            if doesMemberExist(user, groupname):
                c.execute("""
                    DELETE FROM groupmembers
                    WHERE groupname ='{}' AND username = '{}'
                """.format(groupname, user))
                conn.commit()
                c.execute("""
                    UPDATE groups
                    SET members = members - 1
                    WHERE groupname = "{}";
                """.format(groupname))
                conn.commit()
                deleted.append(user)
    except:
        pass
    finally:
        return " ".join(deleted) + " deleted in " + groupname + "\n"

#This function getes the list of members for the given groupname.
def getMembers(username, groupname, forChat = False):
    try:
        if doesMemberExist(username, groupname):
            getMems = c.execute("""
                SELECT *
                FROM groupmembers
                WHERE groupname = '{}'
            """.format(groupname))
            conn.commit()
            members = []
            for member in getMems:
                if not forChat and isGroupOwner(member[2], groupname):
                    members.append(member[2] + "(OWNER)")
                else:
                    members.append(member[2])
            return members
        return []
    except:
        return []

#This function deletes the entire group.
def removeGroup(username, groupname):
    try:
        if isGroupOwner(username, groupname):
            c.execute("""
                DELETE FROM groups
                WHERE groupname ='{}'
            """.format(groupname))
            conn.commit()
            c.execute("""
                DELETE FROM groupmembers
                WHERE groupname ='{}'
            """.format(groupname))
            conn.commit()
            return "Group " + groupname + " deleted"
        else:
            return "Only owner of the group can delete the group."
    except:
        return "Unable to delete the group"