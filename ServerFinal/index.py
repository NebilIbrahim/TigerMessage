import os
from flask import Flask, render_template, send_file
from flask import request
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cas import CAS
from flask_cas import login_required

from flask_heroku import Heroku

import dbopsAttempt
import mlops

app = Flask(__name__)
cas = CAS(app)

app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/' 
app.config['CAS_AFTER_LOGIN'] = 'index'
app.config['SECRET_KEY'] = 'super secret thingy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'#os.environ['DATABASE_URL']#'postgresql://localhost/pre-registration'
io = SocketIO(app)
heroku = Heroku(app)
db = SQLAlchemy(app)
tmp = db.engine
#tmp.execute("CREATE TABLE IF NOT EXISTS fooooo (tmp INTEGER)")


print(tmp)

@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    dbopsAttempt.update_user_table(cas.username, cas.username)
    dbopsAttempt.init_name_table(cas.username)
    if request.method == 'GET':
        return render_template("chats.html", mah_chats=dbopsAttempt.sort_chats(cas.username),
                               username=cas.username)
        # print("foo")
        # print("netid: ", cas.username)
        # return render_template("index.html", username=cas.username)#render_template('index.html')
    if request.method == 'POST':
        print("FOOOOOOO")
        print(request.form['to_chat'])
        dbopsAttempt.read_message(request.form['to_chat'], cas.username)
        return render_template("index.html", username=cas.username, to_chat=request.form['to_chat'])#render_template('index.html')

#@app.route('/')
#@login_required
#def chats_fooooooo():
#    print("bar")
#    return render_template("chats.html")

clients = []
chat = []
uids = []
curToken = 0

@io.on('chat message')

@io.on('connect')
def on_connect():
    global curToken
    print(len(clients))
    io.emit('token', curToken, room=request.sid)
    print("user connected")

@io.on('confirm')
def on_confirm(tok, username, chat_name):
    if tok != curToken:
        print("UH OH!")
    print(dbopsAttempt.is_member(chat_name, username))
    if not dbopsAttempt.is_member(chat_name, username): # ATTN check member
        io.emit('not member', room=request.sid)
        print("NOT MEMBER")
        return None
    else:
        print("WE GOOD")
        clients.append(request.sid)
        chat.append(chat_name)
        io.emit('clear', room=request.sid)
        uids.append(dbopsAttempt.update_user_table("foo", username))
        for (mid, msg, u, tsmp, g) in dbopsAttempt.get_messages(str(chat_name)): ## THIS HAS TO BE EVENTUALLY CHANGED
            io.emit('chat message', data=(u, msg, False), room=request.sid) ## ATTN
        io.emit('confirm', dbopsAttempt.get_chat_name(chat_name), room=request.sid)

@io.on('restrict')
def on_restrict(chat, *words):
    print("FOOOBARB")
    io.emit('clear', room=request.sid)
    restrict_to = 0
    max_cmp = 0.0
    for c in range(10):
        closeness = mlops.sentence_closeness(words, dbopsAttempt.cat_message_words(chat, c))
        if closeness > max_cmp:
            print("ASDFASDFASDF ", closeness, c)
            restrict_to = c
            max_cmp = closeness
    print(dbopsAttempt.get_subject_messages(str(chat), str(restrict_to)))
    for (mid, msg, u, tsmp, g) in dbopsAttempt.get_subject_messages(str(chat), str(restrict_to)):
        io.emit('chat message', data=(u, msg, False), room=request.sid) ## ATTNio.emit(
    io.emit('confirm', dbopsAttempt.get_chat_name(chat), room=request.sid)

@io.on('unrestrict')
def on_unrestrict(chat):
    io.emit('clear', room=request.sid)
    for (mid, msg, u, tsmp, g) in dbopsAttempt.get_messages(str(chat)):
        io.emit('chat message', data=(u, msg, False), room=request.sid) ## ATTNio.emit(
    io.emit('confirm', dbopsAttempt.get_chat_name(chat), room=request.sid)

@io.on('disconnect')
def on_disconnect():
    print("user disconnected")
    #index = clients.index(request.sid)
    #del clients[index]
    #del usernames[index]
    #del chat[index]
    #clients.remove(request.sid)

@io.on('chat message')
def on_message(msg, user, which_chat):
    print("GOT A MESSAGE!")
    index = clients.index(request.sid)
    print("Message from user %s in chat %s" % (user, which_chat))#(usernames[index], chat[index]))
    #print(which_chat)
    #dbopsAttempt.insert_message(msg, str(chat[index]), usernames[index])
    dbopsAttempt.insert_message(msg, str(which_chat), user)
    print(len(clients))
    #io.emit('clear', room=request.sid)
    #for (mid, mesg, u, tsmp, g) in dbopsAttempt.get_messages(str(which_chat)): ## THIS HAS TO BE EVENTUALLY CHANGED
    #    io.emit('chat message', data=(u, str(g) + "| " + mesg), room=request.sid) ## ATTN
    # PROBLEM
    for i in range(len(clients)):
        if chat[i] == which_chat:
            io.emit('chat message', data=(user, msg, True), room=clients[i])

@io.on('new chat')
def on_new_chat(cname, *members):
    print("****")
    print(members)
    print(cname)
    print("****")
    new_id = dbopsAttempt.setup_chat_table(cname, members)
    print("Success")#
    io.emit('refresh', room=request.sid)
    #io.emit('disp', "Chat %s created" % (str(new_id)))

@io.on('change cname')
def change_chat_name(cid, new_name):
    dbopsAttempt.change_chat_name(new_name, cid)
    for i in range(len(clients)):
        if chat[i] == cid:
            io.emit('confirm', new_name, room=clients[i])

def reset_db():
    dbopsAttempt.clear_db()

memIds = ['nbi', 'bwk', 'esthomas', 'nathanl']
memNames = ['Nebil Ibrahim', "Brian Kernighan", 'Emerson Thomas', 'Nathan Lovett-Genovese' ]

if __name__ == '__main__':
    dbopsAttempt.init_db(tmp)
    #print("FOO2")
    #for i in range(0, len(memIds)):
    #    dbopsAttempt.update_user_table(memIds[i], memNames[i])
    #    dbopsAttempt.init_name_table(memIds[i])

    #dbopsAttempt.setup_chat_table("COS333", memIds)

    #dbopsAttempt.add_chat("TEST CHAT")
    io.run(app,
           port=int(os.environ.get('PORT', 5000)),
           #host='0.0.0.0',
           debug=False)
