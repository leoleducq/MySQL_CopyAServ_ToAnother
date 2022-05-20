# MySQL_CopyAServ_ToAnother
### Description
Fait pour migrer des données d'une BDD à une autre
### Pourquoi ?
Ce code a été fait dans le but de migrer des tables d'une BDD à une autre en vérifiant chaque caractère de celle-ci (UTF_8).<br>
Ainsi qu'en modifiant les caractères spéciaux pouvant entrainer des bugs dans un service Web.
### Finalité
Grâce à cette solution, les données sont : 
* Vérifiées 
* Nettoyées
* Normalisées

Le code est évidemment personnalisé pour nos besoins, mais est tout de même accessible à quiconque voulant transférer ou tout simplement nettoyer plus facilement sa BDD.

### Version
| MySQL        | MariaDB           | Python  |
| ------------- |:-------------:| -----:|
| 15.1      | 10.5.15 | 3.9 |

### Installation FR
1. Copier ce répertoire : <code> git clone https://github.com/leoleducq/MySQL_CopyAServ_ToAnother.git </code>
2. Aller dans le dossier "Modules"
3. Modifier le fichier "connect.py" avec les identifiants de connexion à vos BDD
4. Aller dans le dossier "Txt"
5. Modifier le fichier "liste" et mettez le nom des tables à copier
    Syntaxe : nomBDD.nomTable
6. Exécuter main.py : <code>./main.py</code>
7. Dans le dossier "Txt"
* Fichier "?.txt" : Les tuples ayant un "?" dans un de leur champ
* Fichier "errorselect.txt" : Problèmes dans une requête SELECT
* Fichier "errorinsertion.txt" : Les tuples n'ayant pu être insérés
* Fichier "errortable.txt" : Les tables n'ayant pu être créées
* Fichier "newinsert.txt" : Tous les tuples ayant été correctement insérés

### Installation ENG
1. Clone this repository : <code> git clone https://github.com/leoleducq/MySQL_CopyAServ_ToAnother.git </code>
2. Go in the folder "Modules"
3. Modify the file "connect.py" with the login of your BDD
4. Go in the folder "Txt"
5. Modify the file "liste" with the table name you want to copy
    Syntax : BDDname.Tablename
6. Execute main.py : <code>./main.py</code>
7. In the folder "Txt"
* File "?.txt" : The tuple with one "?" in one of their field
* File "errorselect.txt" : Error in a SELECT request
* File "errorinsertion.txt" : The tuple couldn't be insert
* File "errortable.txt" : The table couldn't be create
* File "newinsert.txt" : All the tuple which has been correctly insert
