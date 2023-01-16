from flask import Flask, render_template, request
from pymongo import MongoClient
import os


app = Flask(__name__, template_folder='.')

# Créez une connexion à la base de données MongoDB
client = MongoClient(host='mongodb',
                        port=27017, 
                        username='root', 
                        password='root',
                        authSource="admin")
db = client["db"]

# Récupérez les deux collections dans lesquelles les données sont stockées
collection1 = db["collectiona"]
#collection2 = db["collectionb"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Récupérez le terme de recherche envoyé dans le formulaire
        search_term = request.form.get("search_term")
        
        # Effectuez une recherche dans les deux collections
        documents1 = collection1.find({"nom": {"$regex": search_term, "$options": "i"}})
        documents1 = documents1.sort('prix',1)
        #documents2 = collection2.find({"nom": {"$regex": search_term, "$options": "i"}})

        

        # Affichez les documents dans la vue (template HTML)
        return render_template("index.html", documents1=documents1)


    #Pour vérifier le fichier courant
    with open('text.txt','w' ) as f:
        f.write(os.getcwd())
    
    # Si aucune recherche n'a été effectuée, affichez la page d'accueil
    return render_template("./index.html")

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
