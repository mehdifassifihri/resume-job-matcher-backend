# Guide de Déploiement Railway

Ce guide vous explique comment déployer votre application AI Resume & Job Matcher sur Railway.

## 🚀 Déploiement sur Railway

### Prérequis

1. **Compte Railway** : Créez un compte sur [railway.app](https://railway.app)
2. **Repository GitHub** : Votre code doit être sur GitHub
3. **Clé API OpenAI** : Obtenez votre clé API sur [platform.openai.com](https://platform.openai.com)

### Étapes de Déploiement

#### 1. Préparer le Repository

Assurez-vous que votre repository contient les fichiers suivants :
- `Procfile` - Définit le processus de démarrage
- `railway.json` - Configuration Railway
- `requirements.txt` - Dépendances Python
- `env.example` - Variables d'environnement exemple

#### 2. Connecter à Railway

1. Allez sur [railway.app](https://railway.app) et connectez-vous
2. Cliquez sur "New Project"
3. Sélectionnez "Deploy from GitHub repo"
4. Choisissez votre repository `resume-job-matcher-backend`

#### 3. Configuration des Variables d'Environnement

Dans le dashboard Railway, allez dans l'onglet "Variables" et ajoutez :

```env
# Obligatoire
OPENAI_API_KEY=sk-your-openai-api-key-here
JWT_SECRET_KEY=your-very-secure-secret-key-here

# Optionnel (valeurs par défaut)
DEFAULT_MODEL=gpt-4o-mini
DATABASE_URL=sqlite:///./resume_matcher.db
DEBUG=false
LOG_LEVEL=INFO
```

#### 4. Déploiement Automatique

Railway va automatiquement :
1. Détecter que c'est une application Python
2. Installer les dépendances depuis `requirements.txt`
3. Démarrer l'application avec `python -m src.main`
4. Exposer l'application sur une URL publique

### 🔧 Configuration Avancée

#### Variables d'Environnement Détaillées

| Variable | Obligatoire | Description | Valeur par défaut |
|----------|-------------|-------------|-------------------|
| `OPENAI_API_KEY` | ✅ | Clé API OpenAI | - |
| `JWT_SECRET_KEY` | ✅ | Clé secrète JWT | - |
| `DEFAULT_MODEL` | ❌ | Modèle OpenAI à utiliser | `gpt-4o-mini` |
| `DATABASE_URL` | ❌ | URL de la base de données | `sqlite:///./resume_matcher.db` |
| `DEBUG` | ❌ | Mode debug | `false` |
| `LOG_LEVEL` | ❌ | Niveau de log | `INFO` |
| `PORT` | ❌ | Port d'écoute | `8000` |

#### Modèles OpenAI Supportés

- `gpt-4o-mini` (Recommandé - économique et performant)
- `gpt-4o` (Premium - qualité maximale)
- `gpt-4-turbo` (Équilibré)
- `gpt-3.5-turbo` (Budget)

### 🚨 Résolution de Problèmes

#### Problèmes Courants

1. **Erreur de démarrage**
   - Vérifiez que `OPENAI_API_KEY` est définie
   - Vérifiez que `JWT_SECRET_KEY` est définie
   - Consultez les logs dans Railway dashboard

2. **Erreur de dépendances**
   - Vérifiez que `requirements.txt` est à jour
   - Railway installe automatiquement les dépendances

3. **Erreur de base de données**
   - Railway utilise SQLite par défaut
   - Pour PostgreSQL, ajoutez le service Railway PostgreSQL

#### Logs et Monitoring

- **Logs** : Accessibles dans Railway dashboard > Deployments > Logs
- **Métriques** : CPU, RAM, Réseau dans l'onglet Metrics
- **Health Check** : `/docs` endpoint pour vérifier le statut

### 🔒 Sécurité

#### Bonnes Pratiques

1. **Clés Secrètes**
   - Utilisez des clés JWT longues et aléatoires
   - Ne jamais commiter les clés API dans le code

2. **Variables d'Environnement**
   - Toutes les données sensibles dans Railway Variables
   - Utilisez `env.example` comme référence

3. **HTTPS**
   - Railway fournit automatiquement HTTPS
   - Certificats SSL gérés automatiquement

### 📊 Monitoring et Maintenance

#### Surveillance

- **Uptime** : Railway surveille automatiquement l'application
- **Restart automatique** : En cas d'échec, Railway redémarre l'application
- **Logs centralisés** : Tous les logs dans Railway dashboard

#### Mises à Jour

1. **Code** : Push sur GitHub = déploiement automatique
2. **Dépendances** : Modifiez `requirements.txt` et push
3. **Variables** : Modifiez dans Railway dashboard

### 💰 Coûts Railway

#### Plan Gratuit
- $5 de crédit gratuit par mois
- Suffisant pour développement et tests

#### Plans Payants
- $5/mois pour plus de ressources
- Scaling automatique selon l'usage

### 🔗 URLs et Accès

Après déploiement, Railway fournit :
- **URL publique** : `https://your-app-name.railway.app`
- **Documentation API** : `https://your-app-name.railway.app/docs`
- **Health Check** : `https://your-app-name.railway.app/docs`

### 📝 Exemple de Configuration Complète

```env
# Railway Variables
OPENAI_API_KEY=sk-proj-abc123...
JWT_SECRET_KEY=super-secret-jwt-key-256-bits-long
DEFAULT_MODEL=gpt-4o-mini
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./resume_matcher.db
PORT=8000
```

### 🎯 Prochaines Étapes

1. **Testez l'API** : Utilisez l'interface Swagger sur `/docs`
2. **Configurez un domaine personnalisé** (optionnel)
3. **Ajoutez un service PostgreSQL** pour la production
4. **Configurez les backups** de base de données

---

**🎉 Félicitations !** Votre application AI Resume & Job Matcher est maintenant déployée sur Railway !
