from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Configuration du dossier pour les uploads
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Données simulées
interventions = [
    {
        "type": "Incendie",
        "lieu": "Cocody, Rue des Jardins",
        "statut": "En cours",
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "photo": None
    },
    {
        "type": "Accident",
        "lieu": "Plateau, Avenue Chardy",
        "statut": "Terminé",
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "photo": None
    }
]

casernes = [
    {
        "nom": "Caserne Centrale d'Abidjan",
        "adresse": "Plateau, Avenue Chardy",
        "tel": "+225 27 20 22 48 53"
    },
    {
        "nom": "Caserne de Cocody",
        "adresse": "Cocody, Boulevard Latrille",
        "tel": "+225 27 22 44 64 70"
    }
]

# Route pour servir les fichiers statiques
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Route pour mettre à jour le statut d'une intervention
@app.route('/update_status/<int:intervention_id>', methods=['POST'])
def update_status(intervention_id):
    if 0 <= intervention_id < len(interventions):
        interventions[intervention_id]['statut'] = "Terminée"
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# Route pour supprimer une intervention
@app.route('/delete_intervention/<int:intervention_id>', methods=['POST'])
def delete_intervention(intervention_id):
    if 0 <= intervention_id < len(interventions):
        del interventions[intervention_id]
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# Template principal
template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sapeurs-Pompiers d'Abidjan</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#e63946">
    <link rel="apple-touch-icon" href="/static/images/icon-192x192.png">
    <style>
        :root {
            --primary: #e63946;
            --secondary: #1d3557;
            --accent: #ffd700;
            --background: #f1faee;
            --text: #2b2d42;
            --white: #ffffff;
            --gradient: linear-gradient(135deg, #e63946, #1d3557);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
        }
        
        .navbar {
            background: var(--gradient);
            color: var(--white);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar h1 {
            font-size: 1.8rem;
            font-weight: 600;
            text-align: center;
        }
        
        .hero {
            background: var(--gradient);
            color: var(--white);
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://images.unsplash.com/photo-1582152629442-4a864303fb96?auto=format&fit=crop&w=1920&q=80') center/cover;
            opacity: 0.2;
        }
        
        .hero-content {
            position: relative;
            z-index: 1;
        }
        
        .emergency-number {
            font-size: 3.5rem;
            color: var(--accent);
            margin: 1.5rem 0;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .section-title {
            font-size: 2rem;
            color: var(--secondary);
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            padding-bottom: 1rem;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: var(--primary);
        }
        
        .filter-buttons {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .filter-btn {
            padding: 0.5rem 1.5rem;
            border: none;
            border-radius: 25px;
            background: var(--white);
            color: var(--secondary);
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .filter-btn.active {
            background: var(--secondary);
            color: var(--white);
        }

        .filter-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }
        
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .card {
            background: var(--white);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: var(--primary);
            margin-bottom: 1rem;
            font-size: 1.4rem;
        }
        
        .card p {
            color: var(--text);
            margin: 0.5rem 0;
        }
        
        .intervention-photo {
            margin: 1rem 0;
            border-radius: 8px;
            overflow: hidden;
            max-height: 200px;
        }
        
        .intervention-photo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .btn {
            display: inline-block;
            background: var(--primary);
            color: var(--white);
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(230, 57, 70, 0.4);
        }
        
        .btn-termine {
            background: #4CAF50;
            margin-top: 1rem;
            font-size: 0.9rem;
            padding: 0.5rem 1rem;
        }
        
        .btn-danger {
            background: #dc3545 !important;
        }

        .btn-danger:hover {
            background: #c82333 !important;
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .status-en-cours {
            background: #ffd700;
            color: #000;
        }
        
        .status-termine {
            background: #4CAF50;
            color: white;
        }
        
        .notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 1rem 2rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s ease-out;
            z-index: 1000;
        }
        
        .notification.success {
            background: #4CAF50;
        }
        
        .notification.error {
            background: #f44336;
        }

        .intervention-card {
            display: flex;
            flex-direction: column;
        }

        .intervention-card.hidden {
            display: none;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .intervention-card {
            animation: fadeIn 0.5s ease-out;
        }
        
        @media (max-width: 768px) {
            .hero {
                padding: 3rem 1rem;
            }
            
            .emergency-number {
                font-size: 2.5rem;
            }
            
            .container {
                padding: 0 1rem;
            }
            
            .cards-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1><i class="fas fa-fire-extinguisher"></i> Sapeurs-Pompiers d'Abidjan</h1>
    </nav>
    
    <div class="hero">
        <div class="hero-content">
            <h2>Service d'Urgence 24/7</h2>
            <div class="emergency-number">
                <i class="fas fa-phone"></i> 180
            </div>
            <p>Pour une intervention immédiate, appelez le 180</p>
            <a href="/urgence" class="btn">
                <i class="fas fa-exclamation-triangle"></i> Signaler une Urgence
            </a>
        </div>
    </div>
    
    <div class="container">
        <h2 class="section-title">Interventions</h2>
        
        <div class="filter-buttons">
            <button class="filter-btn active" data-filter="all">
                <i class="fas fa-list"></i> Toutes
            </button>
            <button class="filter-btn" data-filter="en-cours">
                <i class="fas fa-clock"></i> En cours
            </button>
            <button class="filter-btn" data-filter="termine">
                <i class="fas fa-check"></i> Terminées
            </button>
            <button class="btn btn-danger" id="deleteAllCompleted">
                <i class="fas fa-trash"></i> Supprimer les terminées
            </button>
        </div>

        <div class="cards-grid">
            {% for intervention in interventions %}
            <div class="card intervention-card" data-id="{{ loop.index0 }}" data-status="{{ intervention.statut.lower() }}">
                <h3>
                    {% if intervention.type == "Incendie" %}
                        <i class="fas fa-fire"></i>
                    {% elif intervention.type == "Accident" %}
                        <i class="fas fa-car-crash"></i>
                    {% else %}
                        <i class="fas fa-ambulance"></i>
                    {% endif %}
                    {{ intervention.type }}
                </h3>
                {% if intervention.photo %}
                <div class="intervention-photo">
                    <img src="{{ intervention.photo }}" alt="Photo de l'urgence">
                </div>
                {% endif %}
                <p><i class="fas fa-map-marker-alt"></i> {{ intervention.lieu }}</p>
                <p>
                    <span class="status-badge {% if intervention.statut == 'En cours' %}status-en-cours{% else %}status-termine{% endif %}">
                        <i class="fas fa-circle"></i> {{ intervention.statut }}
                    </span>
                </p>
                <p><i class="far fa-clock"></i> {{ intervention.date }}</p>
                {% if intervention.statut == 'En cours' %}
                <button class="btn btn-termine" onclick="terminerIntervention({{ loop.index0 }})">
                    <i class="fas fa-check"></i> Marquer comme terminée
                </button>
                {% else %}
                <button class="btn btn-danger" onclick="supprimerIntervention({{ loop.index0 }})">
                    <i class="fas fa-trash"></i> Supprimer
                </button>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <h2 class="section-title">Nos Casernes</h2>
        <div class="cards-grid">
            {% for caserne in casernes %}
            <div class="card">
                <h3><i class="fas fa-building"></i> {{ caserne.nom }}</h3>
                <div class="contact-info">
                    <i class="fas fa-map-marker-alt"></i>
                    <p>{{ caserne.adresse }}</p>
                </div>
                <div class="contact-info">
                    <i class="fas fa-phone"></i>
                    <p>{{ caserne.tel }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // Fonction de filtrage
        function filterInterventions(status) {
            const cards = document.querySelectorAll('.intervention-card');
            cards.forEach(card => {
                if (status === 'all' || card.dataset.status === status) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        }

        // Gestionnaire des boutons de filtrage
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                filterInterventions(btn.dataset.filter);
            });
        });

        // Fonction de suppression d'une intervention
        function supprimerIntervention(id) {
            if (confirm('Êtes-vous sûr de vouloir supprimer cette intervention ?')) {
                fetch(`/delete_intervention/${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const card = document.querySelector(`.card[data-id="${id}"]`);
                        card.style.animation = 'fadeOut 0.3s ease-out';
                        setTimeout(() => {
                            card.remove();
                        }, 300);
                        showNotification('Intervention supprimée !', 'success');
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    showNotification('Erreur lors de la suppression.', 'error');
                });
            }
        }

        // Fonction pour supprimer toutes les interventions terminées
        document.getElementById('deleteAllCompleted').addEventListener('click', function() {
            if (confirm('Êtes-vous sûr de vouloir supprimer toutes les interventions terminées ?')) {
                const terminatedCards = document.querySelectorAll('.intervention-card[data-status="terminée"]');
                terminatedCards.forEach(card => {
                    const id = card.dataset.id;
                    supprimerIntervention(id);
                });
            }
        });

        // Fonction pour terminer une intervention
        function terminerIntervention(id) {
            if (confirm('Êtes-vous sûr de vouloir marquer cette intervention comme terminée ?')) {
                fetch(`/update_status/${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const card = document.querySelector(`.card[data-id="${id}"]`);
                        const statusBadge = card.querySelector('.status-badge');
                        const button = card.querySelector('.btn-termine');
                        
                        statusBadge.classList.remove('status-en-cours');
                        statusBadge.classList.add('status-termine');
                        statusBadge.innerHTML = '<i class="fas fa-circle"></i> Terminée';
                        
                        card.dataset.status = 'terminée';
                        
                        if (button) {
                            button.outerHTML = `
                                <button class="btn btn-danger" onclick="supprimerIntervention(${id})">
                                    <i class="fas fa-trash"></i> Supprimer
                                </button>
                            `;
                        }
                        
                        showNotification('Intervention marquée comme terminée !', 'success');
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    showNotification('Erreur lors de la mise à jour du statut.', 'error');
                });
            }
        }

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.innerHTML = `
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                ${message}
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def accueil():
    return render_template_string(template, interventions=interventions, casernes=casernes)

@app.route('/urgence', methods=['GET', 'POST'])
def urgence():
    if request.method == 'POST':
        photo = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                filename = f"urgence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = f"/static/uploads/{filename}"

        nouvelle_urgence = {
            "type": request.form.get('type'),
            "lieu": request.form.get('lieu'),
            "statut": "En cours",
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "photo": photo
        }
        interventions.insert(0, nouvelle_urgence)
        return redirect(url_for('accueil'))
    
    form_template = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Signaler une Urgence</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            :root {
                --primary: #e63946;
                --secondary: #1d3557;
                --accent: #ffd700;
                --background: #f1faee;
                --text: #2b2d42;
                --white: #ffffff;
                --gradient: linear-gradient(135deg, #e63946, #1d3557);
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }
            
            body {
                background-color: var(--background);
                color: var(--text);
                line-height: 1.6;
            }
            
            .navbar {
                background: var(--gradient);
                color: var(--white);
                padding: 1rem 2rem;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .form-container {
                max-width: 600px;
                margin: 2rem auto;
                padding: 2rem;
                background: var(--white);
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .form-title {
                color: var(--secondary);
                text-align: center;
                margin-bottom: 2rem;
                font-size: 1.8rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--secondary);
                font-weight: 500;
            }
            
            .form-group select,
            .form-group input {
                width: 100%;
                padding: 0.8rem;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 1rem;
                transition: border-color 0.3s ease;
            }
            
            .form-group select:focus,
            .form-group input:focus {
                outline: none;
                border-color: var(--primary);
            }
            
            .photo-preview {
                max-width: 100%;
                height: 200px;
                border: 2px dashed #ddd;
                border-radius: 8px;
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                position: relative;
            }
            
            .photo-preview img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
            }
            
            .photo-preview.empty {
                background: #f8f9fa;
            }
            
            .photo-preview.empty::after {
                content: 'Aperçu de la photo';
                color: #666;
                font-size: 0.9rem;
            }
            
            .photo-input {
                display: none;
            }
            
            .photo-label {
                display: inline-block;
                padding: 0.8rem 1.5rem;
                background: var(--secondary);
                color: white;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 0.5rem;
                transition: all 0.3s ease;
            }
            
            .photo-label:hover {
                background: #2a4a73;
            }
            
            .btn {
                display: inline-block;
                background: var(--primary);
                color: var(--white);
                padding: 1rem 2rem;
                border: none;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: 500;
                text-decoration: none;
                transition: all 0.3s ease;
                cursor: pointer;
                width: 100%;
                text-align: center;
                box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(230, 57, 70, 0.4);
            }
            
            .btn-secondary {
                background: #666;
                margin-top: 1rem;
            }
            
            .urgence-icon {
                text-align: center;
                font-size: 3rem;
                color: var(--primary);
                margin-bottom: 1rem;
            }
            
            @media (max-width: 768px) {
                .form-container {
                    margin: 1rem;
                    padding: 1.5rem;
                }
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <h1><i class="fas fa-fire-extinguisher"></i> Signaler une Urgence</h1>
        </nav>
        
        <div class="form-container">
            <div class="urgence-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <h2 class="form-title">Formulaire d'Urgence</h2>
            <form method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label><i class="fas fa-list"></i> Type d'urgence:</label>
                    <select name="type" required>
                        <option value="Incendie">Incendie</option>
                        <option value="Accident">Accident</option>
                        <option value="Secours">Secours à personne</option>
                        <option value="Autre">Autre</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label><i class="fas fa-camera"></i> Photo de l'urgence:</label>
                    <input type="file" name="photo" id="photo" class="photo-input" accept="image/*" capture="environment">
                    <label for="photo" class="photo-label">
                        <i class="fas fa-camera"></i> Prendre une photo
                    </label>
                    <div class="photo-preview empty" id="photoPreview"></div>
                </div>
                
                <div class="form-group">
                    <label><i class="fas fa-map-marker-alt"></i> Lieu:</label>
                    <input type="text" name="lieu" required placeholder="Adresse précise de l'urgence">
                </div>
                
                <button type="submit" class="btn">
                    <i class="fas fa-paper-plane"></i> Envoyer l'alerte
                </button>
                
                <a href="/" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Retour
                </a>
            </form>
        </div>
        
        <script>
            const photoInput = document.getElementById('photo');
            const photoPreview = document.getElementById('photoPreview');
            
            photoInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        photoPreview.innerHTML = `<img src="${e.target.result}" alt="Aperçu">`;
                        photoPreview.classList.remove('empty');
                    }
                    reader.readAsDataURL(file);
                } else {
                    photoPreview.innerHTML = '';
                    photoPreview.classList.add('empty');
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)