from flask_login import UserMixin
import unicodedata

class User(UserMixin) : 

    ID = None,
    Date_creation =None,
    Adresse_mail = None,
    TEL = None,
    Pseudo = None,
    Mot_de_passe = None, 	
    Age = None, 
    Poids = None,
    Sexe = None,

    
    def get_id(self):
        return self.ID
"""
    def get_data(self,id):
        if id is not False :
            from .SQL_APP import information_user2
            result = information_user2(ID=id)
            self.ID = result[0][0]
            self.Date_creation = result[0][1]
            self.Adresse_mail = result[0][2]
            self.TEL = result[0][3]
            self.Pseudo = result[0][4]
            self.Mot_de_passe = result[0][5]	
            self.Age = result[0][6] 
            self.Poids = result[0][7]
            self.Sexe = result[0][8]
"""