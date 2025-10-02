# 🚀 Guide Rapide - Déploiement Railway

## Étapes Rapides

### 1. Préparer le Repository
```bash
# Vérifiez que tous les fichiers sont présents
ls -la | grep -E "(Procfile|railway.json|requirements.txt|env.example)"

# Commitez et pushez sur GitHub
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Déployer sur Railway
1. Allez sur [railway.app](https://railway.app)
2. Cliquez "New Project" → "Deploy from GitHub repo"
3. Sélectionnez votre repository
4. Railway détecte automatiquement Python et installe les dépendances

### 3. Configurer les Variables d'Environnement
Dans Railway Dashboard → Variables, ajoutez :

```env
OPENAI_API_KEY=sk-votre-clé-api-openai
JWT_SECRET_KEY=votre-clé-secrète-jwt-très-longue-et-sécurisée
DEFAULT_MODEL=gpt-4o-mini
```

### 4. Vérifier le Déploiement
- Attendez 2-3 minutes pour le déploiement
- Vérifiez les logs dans Railway Dashboard
- Testez l'API sur : `https://votre-app.railway.app/docs`

## 🎯 URLs Importantes

- **API Documentation** : `https://votre-app.railway.app/docs`
- **Health Check** : `https://votre-app.railway.app/docs`
- **Base URL** : `https://votre-app.railway.app`

## ✅ Checklist de Déploiement

- [ ] Repository GitHub à jour
- [ ] `OPENAI_API_KEY` configurée dans Railway
- [ ] `JWT_SECRET_KEY` configurée dans Railway
- [ ] Application accessible sur l'URL Railway
- [ ] Documentation API accessible sur `/docs`
- [ ] Tests d'authentification fonctionnels

## 🆘 En cas de Problème

1. **Vérifiez les logs** dans Railway Dashboard
2. **Vérifiez les variables** d'environnement
3. **Consultez** le guide complet : `docs/RAILWAY_DEPLOYMENT.md`

---

**🎉 Votre application est maintenant en ligne sur Railway !**
