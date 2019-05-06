import sys
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask_sqlalchemy import SQLAlchemy

import mlops
# conn = 0
# cur =
en = 0

def next_cid():
    global en

    (cur_cid,) = en.execute("SELECT cid FROM cur_cid").fetchone()
    en.execute("UPDATE cur_cid SET cid = cid + 1 WHERE cid = %s", (cur_cid,))
    print(cur_cid, "***")
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
    en.execute("CREATE TABLE IF NOT EXISTS %s (mid INTEGER, word TEXT)", (AsIs(str_cid(cid) + "words"),))
    print("*****")
    print(str_cid(cid) + "words")
    en.execute(
        "CREATE TABLE IF NOT EXISTS %s (mid SERIAL PRIMARY KEY, message TEXT, sender TEXT, timestamp TIMESTAMP, category INTEGER)",
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
def read_message(cid, uid):
    global conn
    global cur

    cidInsert = (AsIs(cid),)
    uidInsert = (AsIs(uid),)

    en.execute("UPDATE %s SET readLastMessage = TRUE WHERE cid = %s", (AsIs(uid), AsIs(cid)))

def has_been_read(cid, uid):
    global conn
    global cur

    cidInsert = (AsIs(cid),)
    uidInsert = (AsIs(uid),)

    (status,) = en.execute("SELECT readLastMessage FROM %s WHERE cid = %s", (AsIs(uid), AsIs(cid))).fetchone()
    return status

# Add message to the specfic chat table and update for each user in group that they have not read the last message
def insert_message(message, cid, sender):
    global conn
    global en
    global cur
    cidInsert = AsIs(str_cid(cid))
    messageInsert = (AsIs(message),)
    senderInsert = (AsIs(sender),)
    en.execute("INSERT INTO %s(message, sender, timestamp, category) VALUES(%s, %s, NOW(), -2)", (cidInsert, message, sender))
    (mid,) = en.execute("SELECT mid FROM %s WHERE message=%s", (cidInsert,message)).fetchall()[-1]
    for tok in mlops.tokenize_sentence(message):
        print(str(tok))
        en.execute("INSERT INTO %s VALUES (%s, %s)", (AsIs(str_cid(cid) + "words"), mid, str(tok)))
    mids = en.execute("SELECT mid FROM %s", (cidInsert,)).fetchall()
    recent_mids = mids[max(-20, -len(mids)):-1]
    key_words = []
    for (m,) in recent_mids:
        key_words.append([x for (x,) in en.execute("SELECT word FROM %s WHERE mid=%s", (AsIs(str_cid(cid) + "words"),m)).fetchall()])
    print(key_words)

    groups = [[] for i in range(10)]
    groupless = []
    empty = True
    empty_groups = []
    used = []
    for i in range(len(recent_mids)):
        if empty:
            print("ASDF")
        (m,) = recent_mids[i]
        (cur_cat,) = en.execute("SELECT category FROM %s WHERE mid=%s", (cidInsert, m)).fetchone()
        if cur_cat >= 0:
            print(cur_cat)
            groups[cur_cat].append(m)
            empty = False
            used.append(m)
    for i in range(len(recent_mids)):
        (m,) = recent_mids[i]
        if m in used:
            continue
        key_word_set = key_words[i]
        max_match = 0
        max_cmp = 0.0

        for j in range(len(groups)):
            group = groups[j]
            if len(group) > 0:
                rep = key_words[recent_mids.index((group[0],))]
            else:
                empty_groups.append(j)
                continue
            closeness = mlops.sentence_closeness(rep, key_word_set)
            print("fooFo", closeness, key_word_set, rep)
            if closeness > max_cmp:
                max_cmp = closeness
                max_match = j
        if empty:
            print("fo***")
            empty = False
            groups.append([m])
            en.execute("UPDATE %s SET category = %s WHERE mid = %s", (cidInsert, 0, m))
        elif max_cmp > 0.5:
            print("foo")
            groups[max_match].append(m)
            en.execute("UPDATE %s SET category = %s WHERE mid = %s", (cidInsert, max_match, m))
        #elif max_cmp <= 0.1:
        #    print("FOOO")
        #    en.execute("UPDATE %s SET category = %s WHERE mid = %s", (cidInsert, -1, m))
        #    groupless.append(m)
        elif len(empty_groups) > 0 and max_cmp < 0.5: # ATTN hard-coded values
            print("bar")
            print(empty_groups[0])
            en.execute("UPDATE %s SET category = %s WHERE mid = %s", (cidInsert, empty_groups[0], m))
            groups[empty_groups[0]].append(m)
            del empty_groups[0]
        else:
            print("zap")
            en.execute("UPDATE %s SET category = %s WHERE mid = %s", (cidInsert, max_match, m))
            groups[max_match].append(m)
    print(groups)
    print("*|*")

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
    
    #clear_db()

    en.execute("CREATE SCHEMA IF NOT EXISTS public")
    en.execute("CREATE TABLE IF NOT EXISTS cur_cid (cid INTEGER)")
    (entries,) = en.execute("SELECT COUNT(*) FROM cur_cid").fetchone()
    if entries == 0:
        en.execute("INSERT INTO cur_cid VALUES (0)")

    en.execute("CREATE TABLE IF NOT EXISTS cur_cid (cid INTEGER)")
    en.execute("INSERT INTO cur_cid VALUES (0)")
    init_chats_table()
    init_user_table()


# Return all messages in chat table
def get_messages(cid):
    global conn
    global en
    global cur
 
    cidInsert = AsIs(str_cid(cid))
    print(en.execute("SELECT * FROM %s ORDER BY mid", (cidInsert,)).fetchall())
    return en.execute("SELECT * FROM %s ORDER BY mid", (cidInsert,)).fetchall()

def get_subject_messages(cid, cat):
    global en
    cidInsert = AsIs(str_cid(cid))
    return en.execute("SELECT * FROM %s WHERE category = %s OR category < 0 ORDER BY mid", (cidInsert, str(cat))).fetchall()

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
