#!usr/bin/python3
#from re import TEMPLATE
secret_file=open("/media/jhy/46AE-6494/Projet/id.txt","r")
secret_data=secret_file.readlines()
secret_file.close()
import mysql.connector


try : #Docker configured
    mydb = mysql.connector.connect(
      host="127.0.0.1"
    , port = "3306"
    , user=secret_data[0].strip()
    , password= secret_data[1].strip()
    , database = secret_data[2].strip()
    )
except : #docker base
    
    mydb = mysql.connector.connect(
      host="127.0.0.1"
    , port = "3306"
    , user= secret_data[0].strip()
    , password= secret_data[1].strip()
    )
    
    #pass
    

def create_database(database) :
    mycursor = mydb.cursor()
    request = "CREATE DATABASE {database} ".format(database= database )
    mycursor.execute(request)
    mycursor.close()

#create_database("Foodies")

def show_base():
    mycursor = mydb.cursor()
    request = "SHOW DATABASES"
    mycursor.execute(request)
    for x in mycursor:
     print(x) 
    mycursor.close()

#show_base()

def show_table():
    mycursor = mydb.cursor()
    request = "SHOW TABLES"
    mycursor.execute(request)

    for x in mycursor:
     print(x) 
    mycursor.close()

#show_table()


def create_table_users():
    mycursor = mydb.cursor()

    request_init = "CREATE TABLE USERS "

    ID_USERS = "ID_USERS INT PRIMARY KEY NOT NULL AUTO_INCREMENT"
    CREATION = "CREATION DATETIME DEFAULT (CURRENT_TIMESTAMP()) "
    E_MAIL   = "E_MAIL VARCHAR(25) UNIQUE "
    TEL      = "TEL VARCHAR(10) UNIQUE "
    USERNAME = "USERNAME VARCHAR(25) NOT NULL UNIQUE " 
    PASSWORD = "PASSWORD VARCHAR(255) NOT NULL " 
    AGE      = "AGE INT(3) DEFAULT 0 "
    POIDS    = "KG INT(3)  DEFAULT 0"
    SEXE     = "SEXE VARCHAR(1) DEFAULT 'X' "
    NOM      = "NOM VARCHAR(25) "
    
    request_SQL_LOG     = ID_USERS + "," + CREATION + "," +  E_MAIL + ","  + TEL + ","  +USERNAME + "," + PASSWORD 
    request_SQL_APP     = AGE + "," + POIDS   +  "," + SEXE 
    request_SQL_BONUS   = NOM

    request = request_init + "(" + request_SQL_LOG + "," + request_SQL_APP + "," + request_SQL_BONUS + ")"
    mycursor.execute(request)
    mycursor.close() 

#create_table_users()

def create_table_IMC():
    mycursor = mydb.cursor()

    request_init = "CREATE TABLE IMC "

    ID_USERS = "ID_USERS INT NOT NULL references USERS(USERS_ID) "
    CREATION = "CREATION DATETIME DEFAULT (CURRENT_TIMESTAMP()) "
    IMC      = "IMC FLOAT(4) NOT NULL"
    
    request_SQL_LOG     = ID_USERS 
    request_SQL_APP     = CREATION + "," + IMC 

    request = request_init + "(" + request_SQL_LOG + "," + request_SQL_APP  +")"
    mycursor.execute(request)
    mycursor.close() 

#create_table_IMC()


def alter_table_IMC():
    mycursor = mydb.cursor()

    request_init = "CREATE TABLE IMC "

    request = "alter table IMC ADD CONSTRAINT fk_ID_USERS FOREIGN KEY(ID_USERS) references  USERS(ID_USERS)"

    mycursor.execute(request)
    mycursor.close() 

#alter_table_IMC()
    
def show_elements(Table = 'USERS'):

    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE}".format(TABLE = Table)
    mycursor.execute(request)
    result = mycursor.fetchall()
    mycursor.close() 
    return result

#print(show_elements(Table='DATA'))


def drop_table(table):
    mycursor = mydb.cursor()
    request = "DROP TABLES {table}".format(table = table)
    mycursor.execute(request)
    mydb.commit()
    mycursor.close()
#drop_table("USERS")

def insert_table_USERS(MAIL,USERNAME ,PASSWORD, table = 'USERS',hash = True ):
    try :
        mycursor = mydb.cursor()
        request_init = "INSERT INTO {TABLE}".format(TABLE = table)
        request_table = "(E_MAIL, USERNAME,PASSWORD)"
        
        if hash is True :
            request_value =  "('{MAIL}','{USERNAME}', MD5('{PASSWORD}'))".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
        elif hash is False :
            request_value =  "('{MAIL}','{USERNAME}','{PASSWORD}')".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
        
        request = request_init + request_table + "VALUES" + request_value +";"
        mycursor.execute(request)
        mydb.commit()
        mycursor.close()
        print ("Inscription reussis ! Bienvenu")
    except : 
        print ("Nom d'utilisateurs déja existant, veuillez en choisir un autre")


#show_base()
#create_table_users()
#show_table()
#insert_table_USERS(USERNAME = 'Jhyeon', PASSWORD = 2325, AGE = 28, KG = 94)
#print(show_elements(Table = "DATA"))
#drop_table(table = "DATA")


def creation_user(MAIL,USERNAME ,PASSWORD, table = 'USERS', hash = True):
    mycursor = mydb.cursor()
    request_init = "INSERT INTO {TABLE}".format(TABLE = table)
    request_table = "(E_MAIL, USERNAME,PASSWORD)"
    if hash is True :
        request_value =  "('{MAIL}','{USERNAME}',MD5('{PASSWORD}'))".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
    elif hash is False :
        request_value =  "('{MAIL}','{USERNAME}','{PASSWORD}')".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
    
    request = request_init + request_table + "VALUES" + request_value +";"
    mycursor.execute(request)
    mycursor.close()
    mydb.commit()



def connection_user(MAIL,PASSWORD, table = 'USERS'):
    """
    Request Token users
    """
    mycursor = mydb.cursor()
    request = "SELECT ID_USERS,E_MAIL, PASSWORD,USERNAME FROM {TABLE} WHERE E_MAIL = '{EMAIL}' AND PASSWORD =MD5('{PASSWORD}')".format(TABLE = table, EMAIL =MAIL, PASSWORD = PASSWORD)
    mycursor.execute(request)
    result = mycursor.fetchall()
    mycursor.close()
    ID = result[0][0]
    email = result[0][1]
    password = result[0][2]
    pseudo = result[0][3] 
    mycursor.close()
    return ID,email,password,pseudo

"""
A,B,C,D = connection_user(MAIL = "jhyeon@hotmail.fr", PASSWORD = "Elsa")
print(A)
print(B)
print(C)
print(D)
"""

def information_user(ID,userdata, table = 'USERS'):
    """
    Request ID users for flask login
    """
    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE} WHERE ID_USERS = '{ID}' ".format(TABLE = table, ID=ID)
    mycursor.execute(request)
    result = mycursor.fetchall()

    userdata.ID = result[0][0]
    userdata.Date_creation = result[0][1]
    userdata.Adresse_mail = result[0][2]
    userdata.TEL = result[0][3]
    userdata.Pseudo = result[0][4]
    #userdata.Mot_de_passe = result[0][5]	
    userdata.Age = result[0][6] 
    userdata.Poids = result[0][7]
    userdata.Sexe = result[0][8]
    
    mycursor.close()
    return userdata

def information_user2(ID,table='USERS'):
    """
    Request ID users for flask login
    """
    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE} WHERE ID_USERS = '{ID}' ".format(TABLE = table, ID=ID)
    mycursor.execute(request)
    result = mycursor.fetchall()

    return result

#from userdata import User
#userdata = User()
#userdata.get_data(1)
#data = information_user(1,userdata)
#print(data.Adresse_mail)
#print(userdata.Adresse_mail)

def save_imc(user_id,imc,table = 'IMC'):
   
    mycursor = mydb.cursor()
    request_init = "INSERT INTO {TABLE}".format(TABLE = table)
    request_table = "(ID_USERS,IMC)"

    request_value =  "('{USER_ID}','{IMC}')".format(USER_ID = user_id, IMC = imc)
    
    request = request_init + request_table + "VALUES" + request_value +";"
    mycursor.execute(request)
    mycursor.close()
    mydb.commit()
#save_imc(1,30)

#print(show_elements(Table="IMC"))

def show_sql(table = "DATA",columns = False):
    if columns is True :
        request_init = "SHOW COLUMNS  FROM {TABLE} ".format(TABLE = table)
        request = request_init

        mycursor = mydb.cursor()

        mycursor.execute(request)
        result = mycursor.fetchall()
        mycursor.close()
        col = ''
        for cols in result:
            if col == '':
                col = cols[0]
            else :
                col = col, cols[0]
        col = str(col).replace('(','')
        col = str(col).replace(')','')
        col = str(col).replace('[]','')
        col = str(col).replace("'","")

        result = col
        
    else :
        request_init = "SELECT DISTINCT * FROM {TABLE} ".format(TABLE = table)
        request = request_init

        mycursor = mydb.cursor()

        mycursor.execute(request)
        result = mycursor.fetchall()
        mycursor.close()
    
    return result

#show_sql(columns=True)


def recherche_sql(word, table = "DATA"):
    request_init = "SELECT DISTINCT * FROM {TABLE} ".format(TABLE = table)
    request_where = "WHERE NOM LIKE '{word}%';".format(word = word)

    request = request_init + request_where

    mycursor = mydb.cursor()

    mycursor.execute(request)
    result = mycursor.fetchall()
    mycursor.close()
    return result

def dataframe_to_sql(dataframe,table = "DATA"):
    mycursor = mydb.cursor()
    
    request_init = "INSERT INTO {table}".format(table = table)
    request_table = "NOM,ENERGIE_KCAL,ENERGIE_JONES_KJ,ENERGIE_JONES_KCAL,EAU,PROTEINES,GLUCIDES,LIPIDES,SUCRES,FRUCTOSE,GALACTOSE,GLUCOSE,LACTOSE,MALTOSE,SACCHAROSE,AMIDON,FIBRES,POLYOLS,CENDRES,ALCOOL,ACIDES_ORGANIQUES,CHOLESTEROL,SEL,CALCIUM,CHLORURE,CUIVRE,FER,IODE,MAGNESIUM,MANGANESE,PHOSPHORE,POTASSIUM,SELENIUM,SODIUM,ZINC,RETINOL,BETA_CAROTENE,VITAMINE_D,VITAMINE_E,VITAMINE_K1,VITAMINE_K2,VITAMINE_C,VITAMINE_B1,VITAMINE_B2,VITAMINE_B3,VITAMINE_B5,VITAMINE_B6,VITAMINE_B9,VITAMINE_B12"
        
    for row in dataframe.values :
        result = ''
        for element in row :
            if result == '':
                result = '"{N}"'.format(N=str(element).replace('"',''))
            else :
                result = '{H},"{N}"'.format(H=result,N=str(element).replace('"',''))   
        request =  "{init}({table})  VALUES ({data})".format(init = request_init, table = request_table, data = result) 
        mycursor.execute(request)
    
    mydb.commit()
    mycursor.close()