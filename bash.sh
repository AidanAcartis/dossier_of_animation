#!/bin/bash

# Nom du projet
PROJECT_NAME="firework_project"
APP_NAME="firework"

# Création du répertoire du projet
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# Initialisation du projet Django
django-admin startproject $PROJECT_NAME .

# Création de l'application Django
django-admin startapp $APP_NAME

# Création de la structure des dossiers
mkdir -p $APP_NAME/static/js
mkdir -p $APP_NAME/templates

# Fichiers nécessaires
touch $APP_NAME/static/js/firework.js
touch $APP_NAME/templates/index.html
touch firework_effect.py

# Ajout de l'application dans settings.py
SETTINGS_FILE="$APP_NAME/settings.py"
if ! grep -q "$APP_NAME" "$SETTINGS_FILE"; then
    sed -i "/INSTALLED_APPS = \[/a \ \   '$APP_NAME'," "$SETTINGS_FILE"
fi

# Création des fichiers Python requis
touch $APP_NAME/views.py $APP_NAME/models.py

# Ajout d'une vue simple
echo "from django.http import HttpResponse\n\ndef home(request):\n    return HttpResponse(\"<h1>Bienvenue sur Firework</h1>\")" > $APP_NAME/views.py

# Ajout des URLs
echo "from django.urls import path\nfrom .views import home\n\nurlpatterns = [\n    path('', home, name='home'),\n]" > $APP_NAME/urls.py

# Inclusion des URLs dans le projet principal
echo "from django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    path('', include('$APP_NAME.urls')),\n]" > $PROJECT_NAME/urls.py

# Exécution des migrations
python manage.py migrate

# Lancement du serveur Django
# python manage.py runserver

