# PNJMaker #

Ce projet vise à offrir aux rôlistes un script simple, flexible et paramétrable, pour créer des ensembles de caractéristiques de personnages-non-joueurs à la volée durant une session de jeu de rôle.

![Interface](https://media.discordapp.net/attachments/317577929955737601/910485242324865084/unknown.png)

L'interface graphique sera sujette à changement, mais le coeur de fonctionnalités restera sensiblement le même, sauf si des requêtes pertinentes sont soulevées.

Requiert Python 3.7. Peut être lancé en ligne de commande avec la commande bash 'python main.py'.

```ini
# Ce fichier est éditable selon votre bon loisir.
# Il contient toutes les données nécessaire à l'exécution du programme.
# Les commentaires sont précédés du symbole #.
# La notion de lien symbolique permet de chaîner des éléments entre eux.
# ------------------------------------------
# Items obligatoires ; ce sont des champs référencés en dur dans le code.
Opener:Aa,Ab,Ac,Aq,Er,Es,Et,Eu,Ev,Ey,Ez,Fa,Fe,Fi,Fo,Fu,Fy,Ga,Ge,Gi,Go,Gu,Gy,Ka,Ke,Ki,Ko,Ku,Ky,A,E,I,O,U,Y,X,Z
CloserF:ëna,ta,na,neth,a,sa,lia,ia,mee,ee,e,le,ine,ne,ina,i,ni,ri,ika
CloserM:al,ar,r,n,l,dar,don,dir,dun,nar,r,ar,tun,thul,ul,un,um,inn,in,ur,ish,esh
Middle:a,e,i,o,u,y,hi,ri,ho,fi,no,l,m,n,el,f,w,r
# Le pipe (|) décrit que la ligne est en lien symbolique et va se présenter comme telle : |Champ == Valeur~Sous-champ:val1,val2,val3 ...
# Le pourcent (%) décrit que la ligne va présenter des pourcentages de chance d'apparition. La somme sur une lige doit faire 100.
# ------------------------------------------
# Items facultatifs
#
# ethnie
%Ethnie:60%Alastraar,40%Aiui
# forme des yeux
Yeux:amande,ronds,retroussés
# couleur des yeux
Couleur des yeux:jaunes,verts,gris,verts profond,bleus profond,bleus
# couleur de peau
# NOTE : si on veut placer un default, il faut le mettre en premier dans la liste
Couleur de peau:rose,orangée
|Ethnie == "Alastraar"~Couleur de peau:bleu,vert
|Ethnie == "Aiui"~Couleur de peau:blanc,beige,grisâtre
# couleur des cheveux
|Ethnie == "Aiui"~Couleur des cheveux:noir,brun,châtain foncé,châtain,châtain clair,blond foncé,blond moyen,blond clair,blond très clair,blond platine
# toujours mettre la condition la moins filtrante en haut
%|Age <= 15~Situation familiale:5%foyer,80%famille,10%orphelinat,5%rue
|Age >= 30~Rides:légères,absentes
|Age >= 60~Rides:légères,prononcées
%Regard:10%distrait,5%éteint,5%inexpressif,5%morne,10%perçant,10%préoccupé,10%scrutateur,15%soucieux,5%strabisme,10%vague,5%vide,10%vif
```
Si vous souhaitez personnaliser la base de données sur laquelle se base l'application, modifiez le document texte .ini dans le dossier où se trouve le script 'main.py'  
Une catégorie correspond à une ligne. Attention à ne pas supprimer les lignes nécessaires au bon déroulement du programme ! Vous pouvez en changer les valeurs sans problème.  
Il est possible d'utiliser des émulations d'expressions régulières pour effectuer des choix probabilisés, des filtrages simples ou des filtrages probabilisés !  
Veillez également à ne pas laisser de ligne vide, ou une exception sera levée.  
