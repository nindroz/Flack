import os

from flask import Flask,render_template,request,session,redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdjdkfksajfasdj"
socketio = SocketIO(app)


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
        return render_template("index.html",name=session['displayName'])
    
    else:
        return render_template("index.html",name=session['displayName'])
    
    #loads page for first time when user hasnt submitted a name
    if(name is None):
        return render_template("index.html")

#test purposes
@app.route("/pop")
def pop():
    session.pop("displayName")
    return redirect('/')
