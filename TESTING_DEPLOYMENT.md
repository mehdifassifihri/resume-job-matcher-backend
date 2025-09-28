# 🧪 Déploiement pour Tests (Sans Base de Données)

Cette configuration est optimisée pour un déploiement de test rapide sans base de données persistante.

## ✅ Fonctionnalités Disponibles

- ✅ **Matching de CV/Job** : `/match/run` et `/match/upload`
- ✅ **Validation ATS** : `/ats/validate`
- ✅ **Optimisation ATS** : `/ats/optimize`
- ✅ **Health Check** : `/health`
- ✅ **Documentation API** : `/docs`

## ❌ Fonctionnalités Désactivées (pour les tests)

- ❌ Authentification JWT
- ❌ Historique des analyses
- ❌ Gestion des utilisateurs
- ❌ Base de données persistante

## 🚀 Variables d'Environnement Requises

**SEULEMENT :**
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## 📋 Étapes de Déploiement Railway

1. **Créer le projet :**
   ```bash
   railway init
   ```

2. **Configurer la variable d'environnement :**
   ```bash
   railway variables set OPENAI_API_KEY="votre-clé-openai"
   ```

3. **Déployer :**
   ```bash
   railway up
   ```

## 🧪 Tests Rapides

Une fois déployé, testez :

```bash
# Health check
curl https://votre-app.railway.app/health

# Test de matching (avec des données de test)
curl -X POST "https://votre-app.railway.app/match/run" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Développeur Python avec 3 ans d'\''expérience",
    "job_text": "Nous cherchons un développeur Python senior",
    "model": "gpt-4o-mini"
  }'
```

## ⚠️ Limitations

- **Données temporaires** : Les données sont perdues à chaque redémarrage
- **Pas d'authentification** : Tous les endpoints sont publics
- **Pas d'historique** : Impossible de sauvegarder les analyses

## 🔄 Pour Activer les Fonctionnalités Complètes

Si vous voulez activer l'authentification et la base de données plus tard :

1. Décommentez les lignes dans `src/api/api.py`
2. Ajoutez PostgreSQL : `railway add postgresql`
3. Configurez `JWT_SECRET_KEY`
4. Redéployez : `railway up`

---

**Parfait pour tester rapidement les fonctionnalités principales ! 🎯**
