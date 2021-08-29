#!/usr/bin/python3
from _init_ import *
#Import .PY
from ressources.userdata import User
from ressources import prediction as pred
from ressources import tools as tools
from ressources import SQL_APP as SQL_APP


app = app()
app.secret_key = secret_key[0]

#Definition Log 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.ID = user_id
    return user

@app.route('/', methods=['GET', 'POST'])
def home(): 
    
    if request.method == "POST":
        imc_form = request.form
        taille = int(imc_form["taille"])
        poids = int(imc_form['poids'])
        imc = round((poids)/((taille/100)**2),2)

        if current_user.is_authenticated:
            user_id = current_user.ID
            SQL_APP.save_imc(user_id = str(user_id),imc = imc)
            return render_template('home logged.html',imc = imc) 
        else :
            return render_template('home.html', imc=imc)
    
    else :
        if current_user.is_authenticated:
            return render_template("home logged.html")
        else :    

            return render_template('home.html') 


@app.route('/prediction-picture', methods=['GET', 'POST'])
def prediction_photo(): 
    if request.method == "POST":
        image = request.files['image_users']
        filename = tools.saves_pictures(UPLOAD_FOLDER,image,app)
        resultat = pred.prediction(filename,model =2)
        resultat = tools.translate(resultat, dest = 'fr', short = True)

        apports_cols,apports_row = tools.request_food_local(recherche = resultat,flask = True)

        resultat = "Votre photo semble contenir  :" + resultat
        
        return render_template('from_picture.html', pred = resultat, apports_cols = apports_cols, apports_row = apports_row )
    else :
        return render_template('from_picture.html')

@app.route('/database')
def show_database():
    columns = SQL_APP.show_sql(columns = True)
    columns_list = columns.split(",")
    data = SQL_APP.show_sql()
    return render_template('database.html', data = data,columns = columns_list )


@app.route('/connection', methods=['GET', 'POST'])
def loggin(): 
    if request.method == "POST":
        details = request.form
        adresse_mail = details['adresse_mail']
        password = details['mot_de_passe']

        if adresse_mail == "" or password == "" :
            error =  "Veuillez saisir un utilisateur ou mots de passe"
            return render_template('login.html',error=error)

        try :
            id_user,adresse_mail_base,password_base,pseudo = SQL_APP.connection_user(adresse_mail,password)
            user = User()
            user.ID = id_user
            login_user(user,force= False)
            return render_template('welcome.html',pseudo = pseudo)
        
        except :
            error =  "Utilisateur inconnu ou mot de passe incorecte"
            return render_template('login.html',error=error)
        
    else :
        return render_template('login.html')

@app.route('/deconnection', methods=['GET', 'POST'])
def logout():
    logout_user()

    return  redirect ("/")

@app.route('/inscription',methods=['GET', 'POST'])
def inscription(): 
    if request.method == "POST":
        details = request.form
        adresse_mail = details['adresse_mail']
        pseudo = details['pseudo']
        password = details['mot_de_passe']
        SQL_APP.creation_user(MAIL = adresse_mail, USERNAME = pseudo, PASSWORD = password, hash = True)

        return render_template('inscription_success.html')
    else :
        return render_template('inscription.html')


@app.route('/about')
def about(): 
    return render_template('about.html')

start_app(app)