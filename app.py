import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text

# 1. Încarcă variabilele din .env în memorie
load_dotenv()

app = Flask(__name__)

CORS(app)

# 2. Extrage variabilele folosind os.getenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')



# Configurarea conexiunii către PostgreSQL
# Format: postgresql://utilizator:parola@localhost:port/nume_baza_de_date
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Intreb de sanatate aplicatia ---

@app.route('/healthz', methods=['GET'])
def healthz():
    """Liveness Probe: Verifică dacă procesul Flask rulează."""
    return jsonify({"status": "alive"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness Probe: Verifică dacă baza de date este accesibilă."""
    try:
        # Execută o interogare simplă pentru a vedea dacă DB răspunde
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

# --- Intreb de sanatate aplicatia ---

# Definirea modelului pentru tabelul 'carti'
class Carte(db.Model):
    __tablename__ = 'carti'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(200), nullable=False)

# Ruta pentru a citi toate cărțile
@app.route('/carti', methods=['GET'])
def get_carti():
    toate_cartile = Carte.query.all()
    # Transformăm obiectele din baza de date într-o listă de dicționare (JSON)
    rezultat = [{"nume": carte.nume} for carte in toate_cartile]
    return jsonify(rezultat)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)