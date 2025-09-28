# Déploiement sur Railway

Ce guide explique comment déployer l'application AI Resume & Job Matcher sur Railway.

## Variables d'environnement requises

Configurez ces variables dans Railway :

### Obligatoires
- `OPENAI_API_KEY` - Votre clé API OpenAI
- `JWT_SECRET_KEY` - Clé secrète pour JWT (générez une clé forte)
- `DATABASE_URL` - URL de connexion à la base de données PostgreSQL

### Optionnelles
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Durée d'expiration du token (défaut: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Durée d'expiration du refresh token (défaut: 7)

## Configuration Railway

1. **Base de données PostgreSQL** : Railway fournit automatiquement `DATABASE_URL`
2. **Port** : Railway définit automatiquement la variable `PORT`
3. **Environment** : Railway définit automatiquement `RAILWAY_ENVIRONMENT=true`

## Commandes de déploiement

```bash
# Cloner le repository
git clone <votre-repo>
cd resume-job-matcher-backend

# Déployer sur Railway
railway login
railway init
railway up
```

## Vérification du déploiement

Une fois déployé, testez l'endpoint de santé :
```
GET https://votre-app.railway.app/health
```

## Dépannage

### Erreur d'import
Si vous obtenez des erreurs d'import, vérifiez que le `Procfile` utilise `python -m src.main`

### Base de données
Si la base de données ne se connecte pas, vérifiez que `DATABASE_URL` est correctement configurée

### OpenAI API
Assurez-vous que `OPENAI_API_KEY` est configurée et valide

## Structure des fichiers

- `Procfile` - Commande de démarrage pour Railway
- `runtime.txt` - Version Python requise
- `railway.json` - Configuration Railway
- `requirements.txt` - Dépendances Python
