# Utiliser une image Python légère comme base
FROM python:3.10-slim

# Mettre à jour pip
RUN pip install --upgrade pip


# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

RUN apt-get update
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list 


RUN exit
RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18 

COPY /odbc.ini / 
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini
# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/requirements.txt
COPY api/src /app/src

# Installer les dépendances Python et nettoyer le cache de pip
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Passer les variables d'environnement
ENV SQL_CONNECTION_STRING=${SQL_CONNECTION_STRING}
ENV SECRET_KEY=${SECRET_KEY}

# Exposer le port utilisé par Flask (exemple : 5000)
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "src/main.py"]
