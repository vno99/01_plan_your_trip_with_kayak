---
title: Projet Plan your trip with Kayak
pinned: false
---

# Projet Plan your trip with Kayak

## Description du Projet

Kayak, un moteur de recherche de voyages. Cette société fait partie de Booking Holdings. 
70% des utilisateurs planifiant un voyage souhaitent obtenir davantage d'informations sur leur destination.
L'équipe marketing veut développer une application capable de recommander les meilleurs destinations de voyage en se basant sur des données réelles de prévision météo et d'hôtels.

## Objectifs

* Collecte de données
* Stockage dans un datalake
* ETL
* Visualisation

## Données

* API Nominatim pour obtenir les coordonnées GPS des villes
* API openweathermap.org pour récupérer les données météo des villes
* Scraping de Booking.com pour les données hôtelières

## Structure du projet

* ```data/```: Données exportées
* ```images/```: Images utilisées dans les notebooks
* ```notebook/```: Notebooks Jypiter
* ```scrap_booking/```: Moteur Scrapy pour récupérer les données hôtelières

## Librairies Python
```
python -m pip install -r requirements.txt
```

## Fichier .env à compléter dans le dossier notebook
```
OPENWEATHERMAP_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

BUCKET_NAME=

DBHOST= 
DBUSER= 
DBPASS= 
DBNAME= 
PORT=5432
```
