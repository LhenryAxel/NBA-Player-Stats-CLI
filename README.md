# 🏀 NBA Player Stats CLI

## 📌 Description

NBA Player Stats CLI est un **programme Python en ligne de commande** qui permet de rechercher un joueur NBA et d’afficher ses informations principales (équipe, poste, taille, poids) à partir d’une **API officielle NBA**.

Ce projet a été réalisé dans un **cadre académique** afin de mettre en pratique :

* les fonctions Python
* la gestion des arguments de ligne de commande
* l’utilisation d’une API externe
* les tests unitaires avec pytest

---

## ⚙️ Prérequis

* Python 3.10 ou supérieur
* Une connexion internet

---

## 📦 Installation

1. Cloner le dépôt :

```bash
git clone <url-du-repo>
cd nba_player_cli
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## ▶️ Utilisation

Le programme se lance depuis le terminal avec le nom du joueur en argument.

### Syntaxe

```bash
python project.py "Player Name"
```

### Exemple

```bash
python project.py "Stephen Curry"
```

### Exemple de sortie

```
Player: Stephen Curry
Team: Golden State Warriors
Position: G
Height: 6-2
Weight: 185 lbs
```

---

## ❌ Gestion des erreurs

Le programme affiche un message d’erreur si :

* aucun nom de joueur n’est fourni
* le joueur n’existe pas
* l’API est inaccessible

---

## 🧪 Tests unitaires

Les tests sont écrits avec **pytest** et permettent de vérifier la logique interne du programme sans appeler l’API.

Pour lancer les tests :

```bash
pytest
```

Les fonctions testées incluent :

* la normalisation du nom du joueur
* la sélection du bon joueur parmi plusieurs résultats
* le formatage des informations affichées


---

## 👨‍🎓 Auteur

Projet étudiant réalisé par **Axel Lhenry**

---

## 📝 Remarque

Dans un contexte professionnel, la clé API ne devrait pas être stockée directement dans le code mais dans une variable d’environnement.
Ici, ce choix a été fait pour **simplifier l’utilisation du projet** dans un cadre pédagogique.
