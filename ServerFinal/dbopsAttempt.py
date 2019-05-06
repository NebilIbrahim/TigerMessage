import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

# conn = 0
# cur =
global cur_cid
cur_cid = -1


# Increment chat index for a new chat
def next_cid():
    global cur_cid
    cur_cid += 1
    return cur_cid


# Make a new chat table whose name is its chat id (cid) and whose columns are
# message id, message, sender, and timestamp
def setup_chat_table(chatName, membersNames, membersIds):
    global conn
    global cur

    cid = next_cid()
    print("**", cid)
    # Check if cid exist already with member

    # Make sure lists are of same length
    if (len(membersNames) != len(membersIds)):
        print("Mmmmmm check that again.... in setup_chat_table")
        print("The length of membersNames = " + str(len(membersNames)))
        print("The length of memebersIds = " + str(len(membersIds)))
        return

    cidInsert = (AsIs(str_cid(cid)),)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS %s (mid SERIAL PRIMARY KEY, message TEXT, sender TEXT, timestamp TIMESTAMP)",
        cidInsert)

    # Add each member chat pair Ex: (314159, QuadChat, Nebil Ibrahim) (314159, QuadChat, Emmerson) ...
    for i in range(0, len(membersNames)):
        add_chat(cid, membersIds[i])
        cur.execute("INSERT INTO chats_table VALUES (%s, %s, %s, %s)", (cid, chatName, membersIds[i], membersNames[i]))

    conn.commit()

# Used to make table names for chats since they can't be numbers
def str_cid(cid):
    return "Chat" + str(cid)

# add the chat to the users table
def add_chat(cid, uid):
    global conn
    global cur
    uidInsert = AsIs(uid)
    # Make sure user has a name table
    init_name_table(uid)

    cur.execute("INSERT INTO %s VALUES (%s, NOW(), FALSE)", (uidInsert, cid))

    conn.commit()


# make the table which holds everyone's chats. This holds (cid, chatName, uid, name)
# Ex: (314159, QuadChat, nbi, Nebil Ibrahim) repeats for members of same chat
def init_chats_table():
    global conn
    global cur
    cur.execute("CREATE TABLE IF NOT EXISTS chats_table (cid INTEGER, chatName TEXT, uid TEXT, name TEXT)", )
    conn.commit()

# Make a table of users with columns of university ID, name, and time of last login
# Ex: (nbi, Nebil Ibrahim, March 14, 2019 12:49:43 PM)
def init_user_table():
    global conn
    global cur
    cur.execute("CREATE TABLE IF NOT EXISTS user_table (uid TEXT, name TEXT, lastlogin TIMESTAMP)", )
    conn.commit()


# Insert new user or update their login time
# Ex: (nbi, Nebil Ibrahim, March 14, 2019 12:49:43 PM)
def update_user_table(uid, name):
    global conn
    global cur

    cur.execute("CREATE TABLE IF NOT EXISTS user_table (uid TEXT, name TEXT, lastlogin TIMESTAMP)")
    cur.execute("DELETE FROM user_table WHERE uid = %s", (uid,))
    cur.execute("INSERT INTO user_table VALUES (%s, %s, NOW())", (uid, name))

    conn.commit()


# Entry in nbi table (314159, March 14, 2019 12:49:43 PM, TRUE)
def init_name_table(uid):
    global conn
    global cur

    uidInsert = (AsIs(uid),)
    cur.execute("CREATE TABLE IF NOT EXISTS %s (cid INTEGER, timestamp TIMESTAMP, readLastMessage BOOLEAN)", uidInsert)
    conn.commit()


# Declare message as read in the table (set boolean to true)
def read_message(cid, uid):
    global conn
    global cur

    cidInsert = (AsIs(cid),)
    uidInsert = (AsIs(uid),)

    cur.execute("UPDATE %s SET readLastMessage = TRUE WHERE cid = %s", (AsIs(uid), AsIs(cid)))
    conn.commit()

def has_been_read(cid, uid):
    global conn
    global cur

    cidInsert = (AsIs(cid),)
    uidInsert = (AsIs(uid),)

    cur.execute("SELECT readLastMessage FROM %s WHERE cid = %s", (AsIs(uid), AsIs(cid)))
    (bool,) = cur.fetchone()
    return bool


# Add message to the specfic chat table and update for each user in group that they have not read the last message
def insert_message(message, cid, sender):
    global conn
    global cur
    cidInsert = AsIs(str_cid(cid))
    cur.execute("INSERT INTO %s(message, sender, timestamp) VALUES(%s, %s, NOW())", (cidInsert, message, sender))
    conn.commit()


# Return the name of a chat given a university ID
def get_chat_name(cid):
    global conn
    global cur

    cur.execute("SELECT * FROM chats_table WHERE cid=%s", (cid,))
    (cid, cn, foo, bar) = cur.fetchone()
    return cn


# Change the name of this chat and let all users see it as well
def change_chat_name(chatName, cid):
    global conn
    global cur

    cur.execute("UPDATE chats_table SET chatName = %s WHERE cid = %s", (chatName, cid))
    conn.commit()

# Intialize the database and both the chats table and user table
def init_db():
    global conn
    global cur

    conn = psycopg2.connect("dbname=tmessage")

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS public")

    init_chats_table()
    init_user_table()
    conn.commit()


# Return all messages in chat table
def get_messages(cid):
    global conn
    global cur

    cidInsert = (AsIs(str_cid(cid)),)
    cur.execute("SELECT message FROM %s", cidInsert)
    return cur.fetchall()

# Return all the chats for a given user given a university ID
def get_chats(uid):
    global conn
    global cur

    uidInsert = (AsIs(str_cid(uid)), )
    cur.execute("SELECT * FROM %s", uidInsert)
    return cur.fetchall()

# Return all members in a chat given a chat ID
def get_members(cid):
    global conn
    global cur

    cur.execute("SELECT uid FROM chats_table WHERE cid = %s", (AsIs(cid),))
    return cur.fetchall()

# Return a tuple of chat IDs and chat names in descending order of relevancy
def sort_chats(uid):
    global conn
    global cur

    uidInsert = (AsIs(uid),)
    cur.execute("SELECT cid FROM %s ORDER BY timestamp DESC", uidInsert)
    sorted_chats = cur.fetchall()
    chat_names = []

    for i in range(len(sorted_chats)):
        (cid,) = sorted_chats[i]
        chat_names.append((cid, get_chat_name(cid)))

    return chat_names




# They call me Bobby Tables
def drop_all_tables():
    global conn
    global cur
    cur.execute("DROP SCHEMA public CASCADE")
    conn.commit()

# Close the database
def close_db():
    cur.close()
    conn.commit()

def main():
    memIds = ['nbi', 'bwk', 'esthomas', 'nathanl']
    memNames = ['Nebil Ibrahim', "Brian Kernighan", 'Emerson Thomas', 'Nathan Lovett-Genovese']

    init_db()
    init_chats_table()
    for i in range(0, len(memIds)):
        update_user_table(memIds[i], memNames[i])
        init_name_table(memIds[i])
    setup_chat_table("COS333", memNames, memIds)

    insert_message("I should have gone to Harvard :(", 0, 'nbi')

    k =get_members(0)
    print(k)
    print(get_messages(0))

    change_chat_name("Machine Learning",0)
    insert_message("Hi guys here is the assignment", 0, 'bwk')

    setup_chat_table("KoolKidz", memNames, memIds)
    insert_message("I like this chat better", 1, 'nbi')

    print(sort_chats("nbi"))
    print(read_message(0, "nbi"))
    print(has_been_read(0, "nbi"))

    if (len(sys.argv) >= 2 and sys.argv[1] == "1"):
        drop_all_tables()
    # close_db()

# main()