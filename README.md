# Books To Scrape
## Utilisez les bases de Python pour l'analyse de marché

### :clipboard: Pour faire marcher ces scripts, il vous faut :

*_Python :snake: :_* version 3.10

*_Les librairies Python  :closed_book: :_*  
    beautifulsoup4==4.11.1  
    certifi==2022.12.7  
    charset-normalizer==3.0.1  
    idna==3.4  
    requests==2.28.2  
    soupsieve==2.3.2.post1  
    urllib3==1.26.14  

### Comment ça marche :question::question::question:

 :one:  Téléchargez le repo zip sur github  

 :two:  On viens dézipper l'ensemble de notre repo dans un nouveau dossier que l'on appellera *_Scrapping_*  

 :three:  Il va falloir créer un environnement virtuel. A l'aide du terminal, on vient choisir notre nouveau dossier :arrow_down:  
```
 cd Scrapping

```
On créé ensuite notre environement virtuel :arrow_down:
```
 python -m venv <environment name>

```
Notez que <environment name>  est un nom que vous choississez, mais par convention, il est conseillé d'utiliser *_env_*  

:four: Une fois l'environnement mis en place, il nous faut l'activer :arrow_down:
```
 .//env/Scripts/activate.ps1

```
Normalement, lors de l'activation vous devriez voir (env) devant le chemin :arrow_down:
```
 (env) PS C:\Users\Arthur\desktop\Scrapping>

```

:five: Il faut ensuite télécharger les librairies nécessaires depuis *requirements.txt* :arrow_down: 
```
 pip install -r requirements.text

```

### Nous pouvons maintenant lancer le script Python :rocket:  

Le script *Phase1.py* nous permet de récupérer les données d'un livre, enregistrer dans un fichier csv, ainsi que son illustration en jpg :arrow_down:
```
 python Phase1.py

```

Le script *Phase2.py* nous permet de récupérer les données d'une catégorie de livres enregistrées dans un fichier csv, ainsi que leurs illustrations en jpg :arrow_down:
```
 python Phase2.py

```

Le script *Phase3.py* nous permet de récupérer les données de l'ensemble des catégories de livres enregistrées dans un fichier csv, ainsi que leurs illustrations en jpg :arrow_down:
```
 python Phase3.py

```

Toutes les données sont extraites via le site [Book to Scrape](http://books.toscrape.com/)
