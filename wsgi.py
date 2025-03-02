from app import app
from waitress import serve

if __name__ == "__main__":
    print("Serveur démarré sur http://localhost:8080")
    serve(app, host="0.0.0.0", port=8080)