<<<<<<< HEAD
<<<<<<< Updated upstream
=======
# 🧠 Gestionnaire de QCM — REST API + Vue.js  
**Lucas THOMAS** · **Yasin KESKIN**

---

## 🚀 Fonctionnalités

- Création, édition et suppression de **questionnaires**
- Ajout de **questions ouvertes** et **questions à choix multiples (QCM)**
- Gestion des **réponses attendues** et des  **choix multiples**

---

## 🛠️ Installation

### 📦 Backend — Flask REST API

1. Accéder au dossier du backend :
   ```bash
   cd server
   ```

2. Installer les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Initialiser la base de données (SQLite) :
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Lancer le serveur :
   ```bash
   flask run
   ```

> ℹ️ Par défaut, l’API est disponible sur `http://localhost:5000/api/v1`

---

### 💻 Frontend — Vue.js (Vite)

1. Accéder au dossier du client :
   ```bash
   cd client
   ```

2. Installer les dépendances NPM :
   ```bash
   npm install
   ```

3. Lancer le serveur de développement :
   ```bash
   npm run dev
   ```

> ℹ️ L’interface sera accessible sur `http://localhost:5173`  
> Les appels API sont automatiquement proxifiés vers `http://localhost:5000/api/v1`
>>>>>>> Stashed changes
=======
```bash
flask db init
flask db migrate
flask db upgrade
```
>>>>>>> 6bd262f8e4cc56230cc8a23b00c9851ed49d6fce
