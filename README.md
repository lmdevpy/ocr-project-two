# Projet-2 Utilisez les bases de Python pour l'analyse de marché


## Prérequis
- Avoir Installer `Git` et `Python` et les mettre à jour.

## Récupérer le projet :
```sh
git clone https://github.com/lmdevpy/ocr-project-two.git
```

## Création de l'environnement virtuel

```sh
python -m venv env
```

## Activation de l'environnement virtuel

Une fois l'environnement virtuel créé, vous pouvez l'activer.
Sur Windows, lancez :
```sh
env\Scripts\activate.bat
```
Sur Unix et MacOS, lancez :
```sh
source env/bin/activate
```

## Il faudra ensuite installer les dépendences necessaires au script:
```sh
pip install -r requirements.txt
```

## lancer le scrapping:
```sh
python scrape.py
```

Une fois le script terminé, celui-ci créera un dossier `books-data` dans lequel seront placées les données extraits, classés par catégorie.