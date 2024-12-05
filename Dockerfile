# Utiliser une image Python légère comme base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY /requirements.txt /app/requirements.txt
COPY api/src /app/src

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask (exemple : 5000)
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "src/main.py"]
