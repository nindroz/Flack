import os

from flask import Flask,render_template,request,session,redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from collections import deque

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdjdkfksajfasdj"
socketio = SocketIO(app)

channels={}
grabChannels=[]

@app.route("/",methods=['GET',"POST"])
def index():
    #gets form 
    name=request.form.get("display")
    
    #makes sure that session is null if it doesent exist
    if(not("displayName" in session)):
        session["displayName"]=None
    
    #sets session and logs in
    if(session['displayName']==None):
        session['displayName']=name
        if(session["displayName"]==None):
            #loads page for first time when user hasnt submitted a name
            return render_template("index.html")
    return redirect(url_for('dashboard'))
    
   

@app.route("/dashboard",methods=['post','get'])
def dashboard():
    return render_template("dashboard.html",name=session['displayName'])

#test purposes
@app.route("/pop")
def pop():
    session.pop("displayName")
    return redirect('/')

@app.route("/getChannels",methods=['GET'])
def getChannels():
    return jsonify({"channels":grabChannels})

@app.route("/getMessages/<name>")
def getMessages(name):
    messages=list(channels[name]['messages'])
    users=list(channels[name]['usernames'])
    timestamp=list(channels[name]['times'])
    print("message"+name)
    return jsonify({"messages":messages,"user":users,"timestamp":timestamp})
    
@app.route("/clean")
def clean():
    channels.clear()
    grabChannels.clear()
    return redirect(url_for("index"))

@app.route("/select", methods=['POST'])
def select():
    channel = request.form.get("channel")
    session["currentChannel"]=channel
    print("current: "+session["currentChannel"])
    return "pass"


@socketio.on("make channel")
def channelM(data):
    if(data['name'] in grabChannels):
        return None
    name=data['name']
    grabChannels.append(name)
    channels[name]={}
    channels[name]['messages']=deque(maxlen=100)
    channels[name]["usernames"]=deque(maxlen=100)
    channels[name]["times"]=deque(maxlen=100)
    emit("cast channel", {"channel": name}, broadcast=True)

@socketio.on("send message")
def message(data):
    msg=data['message']
    print("given channel:" + data["channel"])
    channels[data['channel']]['messages'].append(msg)
    channels[data['channel']]["usernames"].append(session["displayName"])
    time = channels[data['channel']]["times"].append(data['timestamp'])
    emit("display message", {"message": msg,"user":session["displayName"],"timestamp":time},broadcast=True)

     




if __name__ == '__main__':
    socketio.run(app)