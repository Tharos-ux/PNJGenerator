#PNJMaker
Ce projet vise à offrir aux rôlistes un script simple, flexible et paramétrable, pour créer des ensembles de caractéristiques de personnages-non-joueurs à la volée durant une session de jeu de rôle.
![Interface](https://media.discordapp.net/attachments/555328372213809153/909890438561951774/unknown.png)
L'interface graphique sera sujette à changement, mais le coeur de fonctionnalités restera sensiblement le même, sauf si des requêtes pertinentes sont soulevées.

Requiert Python 3.7. Peut être lancé en ligne de commande avec la commande bash 'python main.py'.

```ini
# Ce fichier est éditable selon votre bon loisir.
# Il contient toutes les données nécessaire à l'exécution du programme.
# Les commentaires sont précédés du symbole #.
# La notion de lien symbolique permet de chaîner des éléments entre eux.
# ------------------------------------------
# Items obligatoires ; ce sont des champs référencés en dur dans le code.
Opener:Aa,Ab,Ac,Ad,Ae,Af,Ag,Ah,Ai,Aj,Ak,Al,Am,An,O,U,Y,X,Z
CloserF:ëna,ta,na,neth,a,sa,lia,ia,mee,ee,e,le,ine,ne,ina,i,ni,ri,ika
CloserM:al,ar,r,n,l,dar,don,dir,dun,nar,r,ar,tun,thul,ul,un,um,inn,in,ur,ish,esh
Middle:a,e,i,o,u,y,hi,ri,ho,fi,no,l,m,n,el,f,w,r
# Le pipe (|) décrit que la ligne est en lien symbolique et va se présenter comme telle : |Champ=Valeur>Sous-champ:val1,val2,val3 ...
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
|Ethnie=Alastraar>Couleur de peau:bleu,vert
|Ethnie=Aiui>Couleur de peau:blanc,beige,grisâtre
# couleur des cheveux
|Ethnie=Aiui>Couleur des cheveux:noir,brun,châtain foncé,châtain
```
Si vous souhaitez personnaliser la base de données sur laquelle se base l'application, modifiez le document texte .ini dans le dossier où se trouve le script 'main.py'
Une catégorie correspond à une ligne. Attention à ne pas supprimer les lignes nécessaires au bon déroulement du programme ! Vous pouvez en changer les valeurs sans problème.
Veillez également à ne pas laisser de ligne vide, ou une exception sera levée.
