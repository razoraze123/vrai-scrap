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
Pour lancer l'interface graphique, exécute :

```bash
python Modern_GUI_PyDracula_PySide6_or_PyQt6/main.py
```

Tu peux aussi lancer le script en ligne de commande en fournissant l'URL de la page produit :

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

Tu peux aussi personnaliser le *User-Agent* et/ou passer par un proxy :

```bash
python scrape_images.py https://exemple.com/ma-page-produit \
  --user-agent "MonAgent/1.0" --proxy http://127.0.0.1:8080
```

Ces deux options peuvent également être définies via les variables
d'environnement `USER_AGENT` et `PROXY_URL`.

Par défaut, le sélecteur utilisé est `div[data-media-type='image'] img` et les images sont enregistrées dans `./images`.

🖥️ Interface graphique
L'interface utilise maintenant le thème **PyDracula** basé sur PySide6. Lance
`main.py` pour ouvrir la fenêtre puis clique sur le bouton **New** pour démarrer
le scraping. Une boîte de dialogue confirmera la fin de l'opération ou
affichera un message d'erreur en cas de problème.

📁 Structure du projet
bash
Copier
Modifier
. 
├── scrape_images.py                         # Script principal
├── Modern_GUI_PyDracula_PySide6_or_PyQt6/
│   └── main.py                              # Interface graphique PySide6
├── README.md                                # Ce fichier
├── requirements.txt                         # Dépendances Python
└── images/                                  # Dossier généré avec toutes les images récupérées
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

