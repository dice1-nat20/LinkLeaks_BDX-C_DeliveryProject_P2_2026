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



@app.route('/signalement')
def signalement_page():
    return render_template('signalement.html')



DATA_DIR = 'data'
FUITES_FILE = os.path.join(DATA_DIR, 'fuites.json')

# Crée le dossier data et le fichier s'ils n'existent pas
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(FUITES_FILE):
    with open(FUITES_FILE, 'w') as f:
        json.dump([], f)


@app.route('/signaler', methods=['GET', 'POST'])
def signaler():
    if request.method == 'POST':
        # Charger le JSON existant
        with open(FUITES_FILE, 'r+') as file:
            fuites = json.load(file)
            fuite_id = len(fuites) + 1
            # Créer le dictionnaire avec les infos du formulaire
            fuite = {
                "fuite_id": fuite_id,
                "lat": request.form['lat'],
                "lng": request.form['lng'],
                "commentaire": request.form.get('commentaire', ''),
                "photo": request.form.get('photo', '')  # si tu gères upload plus tard
            }
            fuites.append(fuite)
            file.seek(0)
            json.dump(fuites, file, indent=4)

        return redirect(url_for('success'))  # page simple de confirmation
    return render_template('signalement.html')


@app.route('/success')
def success():
    return "<h2>Signalement enregistré ! ✅</h2>"
















if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)