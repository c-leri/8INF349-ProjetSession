# Projet Session

## Utilisation

Vous pouvez lancer l'application et ses services avec la commande `docker compose up` à la racine du projet.

Cela rendra accessible l'api à l'addresse [localhost:5000](http://localhost:5000) et le front-end à l'addresse [localhost:8080](http://localhost:8080).
Cela rendra également accessible en local la base de donnée sur le port `5432` et le cache sur le port `6379`.

## Structure

```
.
├── requirements.txt
├── api8inf349
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── singleton.py
├── tests
│   └── ...
├── Dockerfile
├── ui
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── flake.nix
```

### `requirements.txt`

Liste les dépendances python pour l'API.

### `api8inf349/`

Code de l'application flask qui fournit l'API.

#### `api8inf349/__init__.py`

Définition des routes et de la méthode de création de l'application flask.

#### `api8inf349/models.py`

Définition des entités peewee et des commandes pour initialiser la bd et lancer le worker.

#### `api8inf349/singleton.py`

Définition de singletons pour la base de donnée, le cache et la queue afin d'avoir une instance de chaque accessible partout dans l'application (et dans les test). 

#### `api8inf349/services.py`

Logique de l'application en elle-même.

### `tests/`

Tests pour l'API. Peuvent être lancé avec la commande `python -m pytest` à la racine du projet (nécessite que le cache et la base de données soient actifs et que les variables d'environnements nécessaires pour s'y connecter soient initialisées).

### `Dockerfile`

Fichier définissant l'image docker pour l'API.

### `ui/`

Code du front-end.

#### `ui/Dockerfile`

Fichier définissant l'image docker pour le font-end (serveur nginx qui sert un fichier html).

### `docker-compose.yml`

Fichier de configuration pour docker compose qui définit 4 services, un pour le cache, un pour la base de données, un pour l'api et un pour le front-end.


### `flake.nix`

Fichier définissant des dépendances systèmes (bibliothèques de développement postgres pour le driver python pour postgres). Pas obligatoire, vous pouvez simplement installer ces dépendances en global sur votre système.
