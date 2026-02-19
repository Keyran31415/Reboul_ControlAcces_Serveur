from flask import Flask, render_template ,request
from database import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#*****************************************************************************************
@app.route("/test")
def accueil():
    co = get_connection()
    if co:
        co.close()
        return "Connexion MySQL réussie"
    else:
        return "Erreur de connexion MySQL"

#*****************************************************************************************
@app.route('/affichage_logs')
def affichage_logs():
    co=get_connection()
    curseur = co.cursor()
    requete_sql = "SELECT * FROM logs_acces ORDER BY horodatage DESC "
    curseur.execute(requete_sql)
    logs = curseur.fetchall()
    curseur.close()
    co.close()
    print(logs)
    return render_template('affichage_logs.html', logs=logs)

#*****************************************************************************************

@app.route("/delete")
def delete():
    id_user=17
    co = get_connection()
    curseur = co.cursor()
    requete = "DELETE FROM users WHERE id = %s"
    curseur.execute(requete, id_user)
    co.commit()
    print(curseur.rowcount, "ligne supprimée")
    curseur.close()
    co.close()
    return "Suppression terminée"

#***********************************************************************************

@app.route("/demande_autorisation", methods=["GET", "POST"])
def demande_autorisation():
    if request.method == "POST":
        uid = request.form["uid"]
        zone = int(request.form["zone"])
        co = get_connection()
        curseur = co.cursor()
        requete = "SELECT nom, z_bureaux, z_stock, z_info, z_technique FROM users WHERE code_carte = %s"
        curseur.execute(requete, (uid))
        reponse = curseur.fetchone()
        zone_autorisation = {1 : "z_bureaux", 2 : "z_stock", 3 : "z_info", 4 : "z_technique"}
        zone_demande = zone_autorisation.get(zone)
        autorisation = reponse.get(zone_demande)
        nom = reponse.get("nom")
        return {"nom": nom, "zone": zone, "autorisation": autorisation}
    return "Requete POST nécessaire"

#***********************************************************************************

@app.route("/ajouter_utilisateur", methods=["GET", "POST"])
def ajouter_utilisateur():
    if request.method == "POST":
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        code_carte = request.form["code_carte"]
        activation_carte = request.form["activation_carte"]
        acces_bureau = request.form["acces_bureau"]
        acces_stock = request.form["acces_stock"]
        acces_informatique = request.form["acces_info"]
        acces_technique = request.form["acces_technique"]

        print(prenom, nom, code_carte, activation_carte, acces_bureau, acces_stock, acces_informatique,acces_technique)

        co = get_connection()
        curseur = co.cursor()
        requete = """
            INSERT INTO users (prenom, nom, code_carte,carte_active, z_bureaux, z_stock, z_info, z_technique) 
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s)
        """
        curseur.execute(requete, (prenom, nom, code_carte,activation_carte,acces_bureau,acces_stock,acces_informatique,acces_technique))
        co.commit()
        nb = curseur.rowcount
        curseur.close()
        co.close()
        return render_template("info_retour.html", res=f"{nb} utilisateur ajouté")

    return render_template("ajouter_utilisateur.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

