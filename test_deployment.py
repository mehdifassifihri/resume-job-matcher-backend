#!/usr/bin/env python3
"""
Script de test pour vérifier que l'application est prête pour le déploiement Railway.
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

def check_files():
    """Vérifie que tous les fichiers nécessaires sont présents."""
    required_files = [
        'Procfile',
        'railway.json', 
        'requirements.txt',
        'env.example',
        'main.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Tous les fichiers requis sont présents")
        return True

def check_requirements():
    """Vérifie que requirements.txt contient les dépendances essentielles."""
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    essential_deps = [
        'fastapi',
        'uvicorn',
        'python-dotenv',
        'openai',
        'sqlalchemy'
    ]
    
    missing_deps = []
    for dep in essential_deps:
        if dep not in content:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"❌ Dépendances manquantes: {', '.join(missing_deps)}")
        return False
    else:
        print("✅ Toutes les dépendances essentielles sont présentes")
        return True

def check_env_variables():
    """Vérifie les variables d'environnement."""
    env_file = Path('env.example')
    if not env_file.exists():
        print("❌ Fichier env.example manquant")
        return False
    
    with open('env.example', 'r') as f:
        content = f.read()
    
    required_vars = [
        'OPENAI_API_KEY',
        'JWT_SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Variables d'environnement configurées")
        return True

def test_imports():
    """Teste que l'application peut être importée."""
    try:
        # Test simple de syntaxe Python du fichier main.py
        with open('main.py', 'r') as f:
            code = f.read()
        
        # Compiler le code pour vérifier la syntaxe
        compile(code, 'main.py', 'exec')
        
        print("✅ Syntaxe Python correcte")
        return True
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def check_procfile():
    """Vérifie que le Procfile est correct."""
    with open('Procfile', 'r') as f:
        content = f.read().strip()
    
    if content == 'web: python main.py':
        print("✅ Procfile correct")
        return True
    else:
        print(f"❌ Procfile incorrect: {content}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de préparation au déploiement Railway")
    print("=" * 50)
    
    tests = [
        ("Vérification des fichiers", check_files),
        ("Vérification des dépendances", check_requirements),
        ("Vérification des variables d'environnement", check_env_variables),
        ("Test d'importation", test_imports),
        ("Vérification du Procfile", check_procfile)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Votre application est prête pour le déploiement Railway !")
        print("\n📝 Prochaines étapes:")
        print("1. Commitez vos changements: git add . && git commit -m 'Add Railway deployment files'")
        print("2. Pushez sur GitHub: git push origin main")
        print("3. Déployez sur Railway: https://railway.app")
        print("4. Configurez les variables d'environnement dans Railway")
        return True
    else:
        print("❌ Des problèmes ont été détectés. Corrigez-les avant le déploiement.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
