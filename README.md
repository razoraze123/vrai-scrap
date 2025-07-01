📌 Description
Ce projet est un scraper web automatisé basé sur Selenium + Python, conçu pour extraire toutes les images haute qualité de la page produit d’un site e-commerce.
Ce projet a été conçu dans le cadre d’un exercice Codex visant à démontrer la capacité à :

Manipuler des pages web dynamiques

Intégrer des contre-mesures anti-détection

Gérer le téléchargement de fichiers distants

Concevoir un code modulaire, maintenable et professionnel

🎯 Objectif
Extraire automatiquement toutes les images de la galerie produit visible sur la page suivante :
https://bob-crew.com/products/bob-ficelle-outdoor

Ces images sont ensuite enregistrées localement dans un dossier dédié. Le script peut facilement être adapté à d'autres pages produits du même site (ou d’autres sites similaires) en changeant simplement l’URL.

⚙️ Technologies utilisées
Composant	Rôle
Selenium	Navigation et manipulation de DOM dynamique
webdriver-manager	Installation automatique de ChromeDriver
requests	Téléchargement des images
Python 3.8+	Langage utilisé
CSS Selectors	Pour cibler les éléments DOM

🛠️ Installation
Cloner le repo

bash
Copier
Modifier
git clone https://github.com/ton-utilisateur/product-image-scraper.git
cd product-image-scraper
Créer un environnement virtuel (optionnel mais recommandé)

bash
Copier
Modifier
python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# venv\Scripts\activate    # Sur Windows
Installer les dépendances

bash
Copier
Modifier
pip install -r requirements.txt
Note : Pas besoin d’installer manuellement ChromeDriver. Le script utilise webdriver-manager qui détecte ta version de Chrome et installe le bon driver automatiquement.

🚀 Utilisation
Lance le script en fournissant l'URL de la page produit :

```bash
python scrape_images.py https://exemple.com/ma-page-produit
```

Tu peux indiquer un sélecteur CSS personnalisé :

```bash
python scrape_images.py https://exemple.com/ma-page-produit \
  --selector "div.gallery img"
```

Et choisir un dossier de sortie différent :

```bash
python scrape_images.py https://exemple.com/ma-page-produit \
  --selector "div.gallery img" --output-dir mes_images
```

Par défaut, le sélecteur utilisé est `div[data-media-type='image'] img` et les images sont enregistrées dans `./images`.

🖥️ Interface graphique
Une fenêtre Tkinter permet de lancer le scraping sans passer par la ligne de
commande. Lance simplement `interface.py`, saisis l'URL du produit puis clique
sur **Scraper les images**. Les messages du script apparaîtront directement dans
la fenêtre. Aucune dépendance externe n'est requise pour cette interface.

📁 Structure du projet
bash
Copier
Modifier
.
├── scrape_images.py         # Script principal
├── interface.py             # Petite interface Tkinter
├── README.md                # Ce fichier
├── requirements.txt         # Dépendances Python
└── images/                  # Dossier généré avec toutes les images récupérées
🔐 Contournement de l’anti-scraping
Le projet inclut :

Suppression de navigator.webdriver

Suppression de l’extension enable-automation

Délai random.uniform pour simuler le comportement humain

Ces stratégies permettent de rendre le scraping moins détectable sur des sites utilisant des vérifications JS basiques.

✅ Résultat attendu
Après exécution, tu obtiens :

text
Copier
Modifier
📸 6 images trouvées.
⬇️ Téléchargement image 1: https://...
⬇️ Téléchargement image 2: https://...
...
✅ Toutes les images ont été enregistrées dans le dossier ./images
📌 Pourquoi ce projet est pertinent pour Codex ?
🎯 Ciblé : extraction d’un contenu utile (assets produits) en e-commerce

🧠 Robuste : résiste aux mécanismes simples d’anti-bot

⚙️ Modulaire : facilement adaptable à d’autres cas de scraping

💡 Best practices : structure claire, logique propre, README documenté

🚫 Éthique : respecte robots.txt du site et ne scrape que des pages autorisées

📬 Auteur
🔧 Construit par [Ton Nom / Ton Pseudo GitHub]
📫 Contact : [email / GitHub / LinkedIn selon préférence]

