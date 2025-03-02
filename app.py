from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Données simulées (pour éviter d'utiliser une base de données)
interventions = [
    {
        "type": "Incendie",
        "lieu": "Cocody, Rue des Jardins",
        "statut": "En cours",
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    },
    {
        "type": "Accident",
        "lieu": "Plateau, Avenue Chardy",
        "statut": "Terminé",
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
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

# Template HTML intégré avec design amélioré
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
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(230, 57, 70, 0.4);
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
            background: #4caf50;
            color: white;
        }
        
        .contact-info {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
        }
        
        .contact-info i {
            margin-right: 0.5rem;
            color: var(--primary);
        }
        
        .footer {
            background: var(--secondary);
            color: var(--white);
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
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
        
        /* Styles pour l'installation PWA */
        #installPWA {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--secondary);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: none;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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
        <h2 class="section-title">Interventions en cours</h2>
        <div class="cards-grid">
            {% for intervention in interventions %}
            <div class="card">
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
                <p><i class="fas fa-map-marker-alt"></i> {{ intervention.lieu }}</p>
                <p>
                    <span class="status-badge {% if intervention.statut == 'En cours' %}status-en-cours{% else %}status-termine{% endif %}">
                        <i class="fas fa-circle"></i> {{ intervention.statut }}
                    </span>
                </p>
                <p><i class="far fa-clock"></i> {{ intervention.date }}</p>
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
    
    <footer class="footer">
        <p>&copy; 2024 Sapeurs-Pompiers d'Abidjan. Tous droits réservés.</p>
    </footer>

    <div id="installPWA">
        <i class="fas fa-download"></i> Installer l'application
    </div>

    <script>
        // Service Worker Registration
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js')
                    .then(registration => {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(err => {
                        console.log('ServiceWorker registration failed: ', err);
                    });
            });
        }

        // PWA Installation
        let deferredPrompt;
        const installButton = document.getElementById('installPWA');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installButton.style.display = 'block';
        });

        installButton.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    console.log('Application installée');
                }
                deferredPrompt = null;
                installButton.style.display = 'none';
            }
        });
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
        nouvelle_urgence = {
            "type": request.form.get('type'),
            "lieu": request.form.get('lieu'),
            "statut": "En cours",
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
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
            <form method="POST">
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
    </body>
    </html>
    """
    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 