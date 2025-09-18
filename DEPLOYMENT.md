# 🚀 Guide de Déploiement - AI Resume & Job Matcher

## 🎯 Déploiement sur Render (Recommandé)

### Pourquoi Render ?

- ✅ **Pas de limite de timeout** (contrairement à Railway)
- ✅ **750 heures gratuites/mois**
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **SSL automatique**
- ✅ **Support Python/FastAPI natif**

### Étapes de Déploiement

#### 1. Préparation

```bash
# 1. Fork le repository sur GitHub
# 2. Clone votre fork
git clone https://github.com/VOTRE-USERNAME/resume-job-matcher-backend.git
cd resume-job-matcher-backend

# 3. Vérifiez les fichiers
ls -la
# Vous devriez voir: requirements.txt, src/, render.yaml
```

#### 2. Création du Compte Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte (gratuit)
3. Connectez votre compte GitHub

#### 3. Création du Service Web

1. **Cliquez sur "New +"** → **"Web Service"**
2. **Connectez votre repository GitHub**
3. **Sélectionnez votre fork**
4. **Configurez le service**:
   - **Name**: `ai-resume-job-matcher`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Plan**: `Free`

#### 4. Variables d'Environnement

Dans l'onglet **"Environment"**:

```
OPENAI_API_KEY = votre-clé-api-openai-ici
DEFAULT_MODEL = gpt-4o-mini
PORT = 10000
```

#### 5. Déploiement

1. **Cliquez sur "Create Web Service"**
2. **Attendez 5-10 minutes** pour le build
3. **Votre API sera disponible** à l'URL fournie

### Test du Déploiement

```bash
# 1. Test health check
curl https://votre-app.onrender.com/health

# 2. Test documentation
# Ouvrez https://votre-app.onrender.com/docs

# 3. Test complet
python test_render.py
# (N'oubliez pas de modifier RENDER_URL dans le script)
```

## 🔧 Configuration Avancée

### Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Clé API OpenAI (requis) | - |
| `DEFAULT_MODEL` | Modèle OpenAI | `gpt-4o-mini` |
| `PORT` | Port du serveur | `10000` |

### Limites du Plan Gratuit

- **750 heures/mois** de temps de calcul
- **Pas de limite de timeout** ⭐
- **Déploiements automatiques** depuis GitHub
- **SSL automatique**

## 🐛 Dépannage

### Problèmes Courants

#### Build échoue
```bash
# Vérifiez les logs de build dans Render
# Assurez-vous que requirements.txt est présent
```

#### Service ne démarre pas
```bash
# Vérifiez que OPENAI_API_KEY est configuré
# Vérifiez les logs de démarrage
```

#### Timeout
```bash
# Render n'a pas de limite de timeout
# Si problème persiste, vérifiez les logs
```

### Logs et Monitoring

- **Logs en temps réel** dans le dashboard Render
- **Métriques** de performance disponibles
- **Redémarrage automatique** en cas d'erreur

## 📊 Comparaison des Plateformes

| Plateforme | Timeout | Gratuit | Facile | Recommandé |
|------------|---------|---------|--------|------------|
| **Render** | ❌ Aucun | ✅ 750h/mois | ✅ Très | ⭐⭐⭐⭐⭐ |
| Railway | ❌ 30-60s | ✅ $5/mois | ✅ Oui | ⭐⭐⭐ |
| Vercel | ❌ 10s | ✅ 100GB/mois | ✅ Oui | ⭐⭐ |
| Heroku | ❌ 30s | ❌ Payant | ✅ Oui | ⭐⭐ |

## 🎉 Résultat Final

Une fois déployé, votre API sera disponible à :
- **URL**: `https://votre-app.onrender.com`
- **Documentation**: `https://votre-app.onrender.com/docs`
- **Health Check**: `https://votre-app.onrender.com/health`

## 📞 Support

- **Documentation Render**: [render.com/docs](https://render.com/docs)
- **Support communautaire**: [render.com/community](https://render.com/community)
- **Issues GitHub**: Créez une issue dans ce repository
