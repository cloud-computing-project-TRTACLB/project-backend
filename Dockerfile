# Utiliser une image Python légère comme base
FROM python:3.10-slim

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances système nécessaires pour pyodbc et le pilote ODBC SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    libgssapi-krb5-2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

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
