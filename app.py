from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_DIR = 'data'
UTILISATEURS_FILE = os.path.join(DATA_DIR, 'utilisateurs.json')
FUITES_FILE = os.path.join(DATA_DIR, 'fuites.json')

# Crée le dossier data s'il n'existe pas
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Crée les fichiers JSON s'ils n'existent pas
for f in [UTILISATEURS_FILE, FUITES_FILE]:
    if not os.path.exists(f):
        with open(f, 'w') as file:
            json.dump([], file)

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        with open(UTILISATEURS_FILE, 'r+') as file:
            utilisateurs = json.load(file)
            utilisateur_id = len(utilisateurs) + 1
            user = {
                "utilisateur_id": utilisateur_id,
                "nom": request.form['nom'],
                "prenom": request.form['prenom'],
                "num_tel": request.form['num_tel'],
                "adress_mail": request.form['adress_mail'],
                "IP": request.remote_addr
            }
            utilisateurs.append(user)
            file.seek(0)
            json.dump(utilisateurs, file, indent=4)
        return redirect(url_for('index'))
    return render_template('inscription.html')

# Page signalement
@app.route('/signalement', methods=['GET', 'POST'])
def signalement():
    if request.method == 'POST':
        with open(FUITES_FILE, 'r+') as file:
            fuites = json.load(file)
            fuite_id = len(fuites) + 1
            fuite = {
                "fuite_id": fuite_id,
                "fuite_latitude": request.form['latitude'],
                "fuite_longitude": request.form['longitude'],
                "commentaire": request.form['commentaire'],
                "photo": request.form['photo'],
                "utilisateur_id": int(request.form['utilisateur_id']),
                "statut": "signalée"
            }
            fuites.append(fuite)
            file.seek(0)
            json.dump(fuites, file, indent=4)
        return redirect(url_for('index'))
    return render_template('signalement.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)