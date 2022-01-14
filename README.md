# PNJMaker #

Ce projet vise à offrir aux rôlistes un script simple, flexible et paramétrable, pour créer des ensembles de caractéristiques de personnages-non-joueurs à la volée durant une session de jeu de rôle.

![Interface](https://media.discordapp.net/attachments/878301351753429072/931309209532907550/unknown.png)

L'interface graphique sera sujette à changement, mais le coeur de fonctionnalités restera sensiblement le même, sauf si des requêtes pertinentes sont soulevées.

Requiert Python 3.10,utilisant le structural pattern matching pour la gestion d'expression régulières. Peut être lancé en ligne de commande avec la commande bash 'python3.10 main.py'.


# Structure de la base de données

## Fichier

Le fichier éditable se trouve dans /PNJMaker/code/ et s'intitule data.ini

## Structure

Le fichier est divisé en deux portions : une obligatoire et l'autre facultative.
Les items obligatoires peuvent voir leurs valeurs être modifiées, mais pas leurs noms, ou le programme ne pourra pas s'exécuter.

```ini
# ------------------------------------------
# Items obligatoires ; ce sont des champs référencés en dur dans le code.
Opener: ...
CloserF: ...
CloserM: ...
Middle: ...
# ------------------------------------------
# Items facultatifs
%Ethnie: ...
```

Les lignes en commentaires sont précédés du symbole #.
Une ligne type de la partie facultative se présente comme ceci :

```ini
[%][|Clé ==/!=/>=/<= Valeur[ &/$ Clé ==/!= ....  Valeur~]KEY:[n%]VALUE1,[n%]VALUE2...
```

La notation entre crochets signifie que l'élément est facultatif.
Comme quelques exemples sont toujours plus parlants, en voici quelques-uns :

```ini
# forme des yeux
%Yeux:65%amande,10%ronds,15%retroussés,10%tombants
# couleur des yeux
Couleur_des_yeux:gris,marrons
|Ethnie == "Aiui"~Couleur_des_yeux:jaunes,verts,gris,verts profond
|Ethnie == "Alastraar"~Couleur_des_yeux:bleus profond,bleus,oranges,gris,marrons,azur
# couleur de peau
# NOTE : si on veut placer un default, il faut le mettre en premier dans la liste
# couleur des cheveux
Couleur_des_cheveux:roux clair,roux moyen,noir,brun,châtain foncé,châtain,châtain clair,blond foncé...
|Ethnie == "Alastraar"~Couleur_des_cheveux:bleu,bleu nacré,violet,violet pâle
|Ethnie == "Aiui"~Couleur_des_cheveux:noir,gris,blancs
# coiffure
|Ethnie != "Aiui"~Coupe_de_cheveux:tombants,demi-queue
# toujours mettre la condition la moins filtrante en haut
%|Age <= 15~Situation_familiale:5%foyer,80%famille,10%orphelinat,5%rue
%|Age >= 30~Rides:30%légères,70%absentes
%|Age >= 60~Rides:40%légères,60%prononcées
|Age >= 17~Métier:acrobate,acteur,alchimiste,apothicaire,architecte,armateur,armurier,artiste,assassin....
%Regard:10%distrait,5%éteint,5%inexpressif,5%morne,10%perçant,10%préoccupé,10%scrutateur,15%soucieux...
# identité de genre
%Identité_de_genre:5%transgenre,95%cisgenre
# orientation sexuelle
#%Orientation_sexuelle:10%homosexuel,5%asexuel,5%bisexuel,80%hétérosexuel
%|Sexe_biologique == "Féminin"~Orientation_sexuelle:10%homosexuelle,5%asexuelle,5%bisexuelle,80%hétérosexuelle
%|Sexe_biologique == "Masculin"~Orientation_sexuelle:10%homosexuel,5%asexuel,5%bisexuel,80%hétérosexuel
# approche multifactorielle. Est soutenu par des expressions régulières.
%|Ethnie == "Alastraar" & Age >= 15~Entend_les_murmures:30%oui,70%non
```

Le pipe (|) décrit que la ligne est en lien symbolique et va se présenter comme telle : |Champ == Valeur~Sous-champ:val1,val2,val3 ...  
Le pourcent (%) décrit que la ligne va présenter des pourcentages de chance d'apparition. La somme sur une lige doit faire 100.  
L'espérluette (&) et le dollar ($) correspondent respectivement aux AND et OR logiques.  
Exemple : %|Ethnie == "Alastraar" & Age >= 15~Entend_les_murmures:30%oui,70%non  

Ce fichier est éditable selon votre bon loisir.

## Notes de fin

Si vous souhaitez personnaliser la base de données sur laquelle se base l'application, modifiez le document texte .ini dans le dossier où se trouve le script 'main.py'  
Une catégorie correspond à une ligne. Attention à ne pas supprimer les lignes nécessaires au bon déroulement du programme ! Vous pouvez en changer les valeurs sans problème.  
Il est possible d'utiliser des expressions régulières pour effectuer des choix probabilisés, des conditionnelles simples, des filtrages simples ou des filtrages probabilisés !  
Veillez également à ne pas laisser de ligne vide, ou une exception sera levée.  
