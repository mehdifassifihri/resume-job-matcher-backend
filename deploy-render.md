# 🚀 Guide de Déploiement Render

## Étapes de Déploiement

### 1. Préparation du Repository

1. **Fork le repository** sur votre compte GitHub
2. **Clone votre fork** localement
3. **Vérifiez que tous les fichiers sont présents**:
   - `requirements.txt`
   - `src/main.py`
   - `render.yaml`

### 2. Création du Compte Render

1. Allez sur [render.com](https://render.com)
2. **Créez un compte** (gratuit)
3. **Connectez votre compte GitHub**

### 3. Création du Service Web

1. **Cliquez sur "New +"** → **"Web Service"**
2. **Connectez votre repository GitHub**
3. **Sélectionnez votre fork** du projet
4. **Configurez le service**:
   - **Name**: `ai-resume-job-matcher` (ou votre nom préféré)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Plan**: `Free`

### 4. Configuration des Variables d'Environnement

Dans l'onglet **"Environment"** de votre service Render :

```
OPENAI_API_KEY = votre-clé-api-openai-ici
DEFAULT_MODEL = gpt-4o-mini
PORT = 10000
```

### 5. Déploiement

1. **Cliquez sur "Create Web Service"**
2. **Attendez le déploiement** (5-10 minutes)
3. **Votre API sera disponible** à l'URL fournie

### 6. Test du Déploiement

```bash
# Test health check
curl https://votre-app.onrender.com/health

# Test API documentation
# Ouvrez https://votre-app.onrender.com/docs dans votre navigateur
```

## 🔧 Configuration Avancée

### Variables d'Environnement Disponibles

- `OPENAI_API_KEY`: Votre clé API OpenAI (requis)
- `DEFAULT_MODEL`: Modèle OpenAI à utiliser (défaut: gpt-4o-mini)
- `PORT`: Port du serveur (défaut: 10000)

### Limites du Plan Gratuit

- **750 heures/mois** de temps de calcul
- **Pas de limite de timeout** (contrairement à Railway)
- **Déploiements automatiques** depuis GitHub
- **SSL automatique**

## 🐛 Dépannage

### Problèmes Courants

1. **Build échoue**:
   - Vérifiez que `requirements.txt` est présent
   - Vérifiez les logs de build dans Render

2. **Service ne démarre pas**:
   - Vérifiez que `OPENAI_API_KEY` est configuré
   - Vérifiez les logs de démarrage

3. **Timeout**:
   - Render n'a pas de limite de timeout comme Railway
   - Si problème persiste, vérifiez les logs

### Logs et Monitoring

- **Logs en temps réel** dans le dashboard Render
- **Métriques** de performance disponibles
- **Redémarrage automatique** en cas d'erreur

## 📞 Support

- **Documentation Render**: [render.com/docs](https://render.com/docs)
- **Support communautaire**: [render.com/community](https://render.com/community)
