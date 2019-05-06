import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask_sqlalchemy import SQLAlchemy

# conn = 0
# cur =
en = 0

global cur_cid
cur_cid = -1


def next_cid():
    global cur_cid
    cur_cid += 1
    return cur_cid



# Make a new chat table whose name is its chat id (cid) and whose columns are
# message id, message, sender, and timestamp
def setup_chat_table(chatName, membersIds):
    global conn
    global en
    global cur

    cid = next_cid()
    print("**", cid)
    # Check if cid exist already with member

    # Make sure lists are of same length
    #if (len(membersNames) != len(membersIds)):
    #    print("Mmmmmm check that again.... in setup_chat_table")
    #    print("The length of membersNames = " + str(len(membersNames)))
    #    print("The length of memebersIds = " + str(len(membersIds)))
    #    return

    cidInsert = (AsIs(str_cid(cid)),)
    chatNameInsert = (AsIs(chatName),)
    en.execute(
        "CREATE TABLE IF NOT EXISTS %s (mid SERIAL PRIMARY KEY, message TEXT, sender TEXT, timestamp TIMESTAMP)",
        cidInsert)

    # Add each member chat pair Ex: (314159, QuadChat, Nebil Ibrahim) (314159, QuadChat, Emmerson) ...
    for i in range(0, len(membersIds)):
        #memberName = (AsIs(membersNames[i]),)
        #memberId = (AsIs(membersIds[i]),)
        add_chat(cid, membersIds[i])
        en.execute("INSERT INTO chats_table VALUES (%s, %s, %s, %s)", (cid, chatName, membersIds[i], membersIds[i]))

    # en.execute("INSERT INTO mids VALUES (0)")
##    conn.commit()


def str_cid(cid):
    return "Chat" + str(cid)


def add_chat(cid, uid):
    global conn
    global en
    global cur
    uidInsert = AsIs(uid)
    # Make sure user has a name table
    init_name_table(uid)

    en.execute("INSERT INTO %s VALUES (%s, NOW(), FALSE)", (uidInsert, cid))

#    conn.commit()


# make the table which holds everyone's chats. This holds (cid, chatName, uid, name)
# Ex: (314159, QuadChat, nbi, Nebil Ibrahim) repeats for members of same chat
def init_chats_table():
    global conn
    global en
    global cur
    en.execute("CREATE TABLE IF NOT EXISTS chats_table (cid INTEGER, chatName TEXT, uid TEXT, name TEXT)", )
#    conn.commit()


def init_user_table():
    global conn
    global en
    global cur
    en.execute("CREATE TABLE IF NOT EXISTS user_table (uid TEXT, name TEXT, lastlogin TIMESTAMP)", )
#    conn.commit()


# Insert new user or update their login time
# (nbi, Nebil Ibrahim, March 14, 2019 12:49:43 PM)
def update_user_table(uid, name):
    global conn
    global en
    global cur
    uidInsert = (AsIs(uid),)
    nameInsert = (AsIs(name),)
    # loginTimeInsert = (AsIs(loginTime),)

    # If they are not a new user just update their most recent login. Else insert them into the
    en.execute("CREATE TABLE IF NOT EXISTS user_table (uid TEXT, name TEXT, lastlogin TIMESTAMP)")
    # en.execute("IF EXISTS UPDATE user_table SET lastlogin = NOW() WHERE uid = %s ", uidInsert)
    # en.execute("ELSE INSERT INTO user_table(uid, name, lastlogin) VALUES(%s, %s, NOW())", uidInsert, nameInsert)
    # ON CONFLICT UNIQUE (uid) DO UPDATE SET lastlogin = NOW()
    en.execute("DELETE FROM user_table WHERE uid = %s", (uid,))
    en.execute("INSERT INTO user_table VALUES (%s, %s, NOW())", (uid, name))

#    conn.commit()


# Entry in nbi table (314159, March 14, 2019 12:49:43 PM, TRUE)
def init_name_table(uid):
    global conn
    global en
    global cur

    uidInsert = (AsIs(uid),)
    en.execute("CREATE TABLE IF NOT EXISTS %s (cid INTEGER, timestamp TIMESTAMP, readLastMessage BOOLEAN)", uidInsert)
#    conn.commit()


# Declare message as read in the table (set boolean to true)
def message_read(cid, uid):
    global conn
    global en
    global cur

    cidInsert = (AsIs(cid),)
    uidInsert = (AsIs(uid),)

    en.execute("UPDATE %s SET readLastMessage = TRUE WHERE cid = %s", uidInsert, cidInsert)

# Add message to the specfic chat table and update for each user in group that they have not read the last message
def insert_message(message, cid, sender):
    global conn
    global en
    global cur
    cidInsert = AsIs(str_cid(cid))
    messageInsert = (AsIs(message),)
    senderInsert = (AsIs(sender),)
    en.execute("INSERT INTO %s(message, sender, timestamp) VALUES(%s, %s, NOW())", (cidInsert, message, sender))

def get_chat_name(cid):
    global conn
    global en
    global cur

    (cid, cn, foo, bar) = en.execute("SELECT * FROM chats_table WHERE cid=%s", (cid,)).fetchone()
    return cn


def change_chat_name(chatName, cid):
    global conn
    global en
    global cur

    chatNameInsert = (AsIs(chatName))
    cidInsert = (AsIs(cid),)
    en.execute("UPDATE chats_table SET chatName = %s WHERE cid = %s", (chatName, cid))

def clear_db():
    global en

    try: # Only uncomment in non-heroku environment
        rows = en.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name").fetchall()
        for row in rows:
            print("dropping table: ", row[1])
            en.execute("drop table " + row[1] + " cascade")
    except:
        print("Error: ", sys.exc_info()[1])
    en.execute("CREATE SCHEMA IF NOT EXISTS public")


def init_db(engine):
    global conn
    global en
    global cur

    en = engine
    
    en.execute("CREATE SCHEMA IF NOT EXISTS public")

    init_chats_table()
    init_user_table()


# Return all messages in chat table
def get_messages(cid):
    global conn
    global en
    global cur
 
    cidInsert = (AsIs(str_cid(cid)),)
    return en.execute("SELECT * FROM %s", cidInsert).fetchall()

def get_chats(uid):
    global conn
    global en
    global cur

    uidInsert = (AsIs(str_cid(uid)), )
    return en.execute("SELECT * FROM %s", uidInsert).fetchall()

def get_members(cid):
    global conn
    global en
    global cur

    cidInsert = (AsIs(str_cid(cid)),)
    return en.execute("SELECT uid FROM chats_table WHERE cid = %s", (AsIs(cid),)).fetchall()

def is_member(cid, uid):
    members = get_members(cid)
    print(members) # 1029
    for (usr,) in members:
        if usr == uid:
            return True
    return False

# Return a tuple of chat IDs and chat names in descending order of relevancy
def sort_chats(uid):
    global en

    uidInsert = (AsIs(uid),)
    sorted_chats = en.execute("SELECT cid FROM %s ORDER BY timestamp DESC", uidInsert).fetchall()
    chat_names = []

    for i in range(len(sorted_chats)):
        (cid,) = sorted_chats[i]
        chat_names.append((cid, get_chat_name(cid)))

    return chat_names

# They call me Bobby Tables
def drop_all_tables():
    global conn
    global en
    global cur
    en.execute("DROP SCHEMA public CASCADE")

def close_db():
    cur.close()
