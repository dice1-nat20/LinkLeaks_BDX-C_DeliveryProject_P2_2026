from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- 1. CONFIGURATION MYSQL ---
# Remplace 'TON_MDP' par le mot de passe de ton utilisateur root dans Workbench
# 'localhost' fonctionne car MySQL est sur le même ordinateur
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:TON_MDP@localhost/fuites_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 2. CONFIGURATION DES DOSSIERS ---
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- 3. MODÈLES (Correspondant à ton SQL) ---

class Fuite(db.Model):
    __tablename__ = 'fuite'
    fuite_id = db.Column(db.Integer, primary_key=True)
    fuite_latitude = db.Column(db.Numeric(9,6), nullable=False)
    fuite_longitude = db.Column(db.Numeric(9,6), nullable=False)

class Signaler(db.Model):
    __tablename__ = 'signaler'
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(100))
    statut = db.Column(db.String(50), default="En attente")
    photo = db.Column(db.String(100))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateur_id'))
    fuite_id = db.Column(db.Integer, db.ForeignKey('fuite.fuite_id'))

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    utilisateur_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    IP = db.Column(db.String(100))

# --- 4. ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signaler', methods=['POST'])
def signaler():
    try:
        # 1. Récupération des données du formulaire
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        comm = request.form.get('commentaire', 'Aucun commentaire')
        
        # 2. Gestion de la photo
        file = request.files.get('photo')
        filename = ""
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 3. Insertion dans la table 'fuite' (Coordonnées)
        nouvelle_pos = Fuite(fuite_latitude=lat, fuite_longitude=lng)
        db.session.add(nouvelle_pos)
        db.session.flush() # Permet de récupérer l'ID avant le commit final

        # 4. Insertion dans la table 'signaler'
        # Note : utilisateur_id est laissé vide ou à 1 pour ce test
        nouveau_signalement = Signaler(
            commentaire=comm,
            photo=filename,
            fuite_id=nouvelle_pos.fuite_id,
            statut="Signalé"
        )
        db.session.add(nouveau_signalement)
        
        # 5. Validation finale en BDD
        db.session.commit()

        return """
        <script>
            alert('Signalement bien reçu !');
            window.location.href = '/';
        </script>
        """
    except Exception as e:
        db.session.rollback()
        return f"Erreur : {str(e)}", 500
    
    except Exception as e:
        db.session.rollback() # Annule tout en cas d'erreur
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/admin')
def admin():
    # On récupère tous les signalements et on joint la table fuite 
    # pour avoir les coordonnées GPS en même temps
    tous_les_signalements = db.session.query(Signaler, Fuite).join(Fuite, Signaler.fuite_id == Fuite.fuite_id).all()
    
    return render_template('admin.html', signalements=tous_les_signalements)

# --- 5. LANCEMENT ---
if __name__ == '__main__':
    # host='0.0.0.0' pour le WiFi, ssl_context='adhoc' pour HTTPS (Caméra/GPS)
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=True)
