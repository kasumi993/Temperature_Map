# Temperature_Project

Projet d'application Web ECL semestre 6 pour l'année 2020-2021

Membres du groupe:
Khady Gueye
Vitor Miranda Gomes
Mouhamed Abba Dan Dodo


**Application à développer**

Le but de ce projet est de fournir une carte glissante sur laquelle sont positionnées les stations météorologiques françaises et, lorsqu’on clique sur l’une d’entre elles, de visualiser l’historique des températures. La visualisation devra permettre de choisir une date de début et de fin et éventuellement d’autres paramètres. On peut envisager par exemple de proposer d’afficher les courbes avec d’autres pas de temps (par défaut : la journée), de faire de l’agrégation de données sur plusieurs stations, de faire des moyennes par jour de l’année sur 40 ans, etc.


Les données originelles sont disponibles sur le site de European Climate Assessment & Dataset project :
https://www.ecad.eu/dailydata/index.php
Remarque : ces données sont également accessibles (de manière plus détaillée) sur le site de données ouvertes de Météo
France (https://donneespubliques.meteofrance.fr/) mais seulement depuis 1996…


**Prise en main et installation:**

D'abord, il faut cloner le projet. Ensuite, il faut lancer le serveur(le fichier http_serveur.py).
Il démarre sur le port 80.
Après, sur le navigateur taper : "localhost:80" ,ce qui va démarrer l’application sur le navigateur.


**Utilisation/fonctionnalité**

Une fois que l’application est demarrée il faut lire ce que le petit bonhomme (Kiwi) dit ;).
Le premier choix que vous devez faire c'est par rapport au Filtrage : Il faut choisir soit un filtrage par Station en France soit par toute la France (pays).

NB: l'application ne génère pas correctement les courbes sur l'option pays, donc nous vous conseillons de choisir l'option station.

Alors, si on prend station comme paramètre du filtre, le prochain pas c'est choisir le période sur laquelle on veut se renseigner.
Pour la période il faut **cliquer sur l’icone calendrier à droite** pour afficher le calendrier (Cela va être plus facile que de taper la date).
Il faut choisir la date de début et date de fin dans la fenêtre.
Une fois la date choisie, on appui sur un marqueur sur la carte.
Le nom de la station s’affichera et bien aussi les courbes.
Pour cette période on peut sélectionner d'autres marqueurs et visualiser des données.


Il y a encore la possibilité de faire une recherche sur la barre de recherche, on commence avec "T" par exemple, ensuite les suggestions s’affichent, et lorsque l’on clique sur une station suggérée, la carte va zoomer sur cette station et on peut enuite la selectionner.

Voila! Have Fun With our App!!

