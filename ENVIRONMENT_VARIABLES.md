# Variables d'environnement

## Variables obligatoires

### OPENAI_API_KEY
- **Description** : Clé API OpenAI pour utiliser les modèles GPT
- **Exemple** : `sk-...`
- **Comment obtenir** : https://platform.openai.com/api-keys

### JWT_SECRET_KEY
- **Description** : Clé secrète pour signer les tokens JWT
- **Exemple** : `your-very-secure-secret-key-change-this-in-production`
- **Génération** : Utilisez un générateur de clés sécurisé

## Variables automatiques (Railway)

### DATABASE_URL
- **Description** : URL de connexion PostgreSQL fournie automatiquement par Railway
- **Format** : `postgresql://user:password@host:port/database`

### PORT
- **Description** : Port sur lequel l'application doit écouter
- **Valeur** : Définie automatiquement par Railway

### RAILWAY_ENVIRONMENT
- **Description** : Indique que l'application s'exécute sur Railway
- **Valeur** : `true`

## Variables optionnelles

### ACCESS_TOKEN_EXPIRE_MINUTES
- **Description** : Durée d'expiration du token d'accès (en minutes)
- **Défaut** : `30`

### REFRESH_TOKEN_EXPIRE_DAYS
- **Description** : Durée d'expiration du refresh token (en jours)
- **Défaut** : `7`

## Configuration pour le déploiement

### Local (.env file)
```env
OPENAI_API_KEY=sk-your-key-here
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./resume_matcher.db
```

### Railway (Variables d'environnement)
```
OPENAI_API_KEY=sk-your-key-here
JWT_SECRET_KEY=your-secret-key
# DATABASE_URL est fournie automatiquement
```
