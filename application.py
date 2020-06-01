import os

from flask import Flask,render_template,request,session,redirect, url_for, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdjdkfksajfasdj"
socketio = SocketIO(app)

channels=[]
messages={}

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

@socketio.on("make channel")
def channelM(data):
    name=data['name']
    print(f"Hello")
    print(name)
    channels.append(name)
    emit("display name", {"channelName":name}, broadcast=True)
