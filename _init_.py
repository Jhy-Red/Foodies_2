#!/usr/bin/python3
try:
    secret_key_file=open("/media/jhy/46AE-6494/Projet/id.txt","r")
    secret_key=secret_key_file.readlines()
    secret_key_file.close()
except :
    secret_key_file=open("C:/Users/User/Documents/Projets.id.txt","r")
    secret_key=secret_key_file.readlines()
    secret_key_file.close()
#Stockage serveur
UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def app():
    """
    init the application on Flask

    return app
    """

    from flask import Flask
    return Flask(__name__
                , static_url_path= '/static'
                )

def start_app(app,host = '0.0.0.0', debug = True) :
    """
    Start the Flask server
    
    app : require app create by app

    host : input IP

    debug : False or True
    """

    app.run(
    host= host
    ,debug = debug
    )

    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





# Import des fonctions Flask
from flask import render_template ,request,redirect
# Import des fonctions Login
from flask_login import LoginManager,login_user,logout_user,current_user