# Raficoin Network

Raficoin Network est une blockchain décentralisée conçue pour offrir des transactions rapides, sécurisées et transparentes. Ce projet inclut un système de récompenses pour les mineurs, un token natif (MessdakToken), et des fonctionnalités de gestion de nœuds.

---

## Fonctionnalités principales
- **Minage** : Récompenses pour les mineurs en RafiCoin.
- **Transactions signées** : Sécurisation des transactions avec des signatures numériques.
- **Gestion des nœuds** : Support pour des réseaux distribués avec des mécanismes de consensus pour résoudre les conflits.
- **API REST** : Interagissez avec la blockchain via des endpoints Flask.
- **Token natif** : RafiCoin avec une offre totale de 21,000,000 tokens.

---

## Installation

1. **Cloner le projet**
   ```bash
   git clone <URL-DU-DEPOT>
   cd RaficoinNetwork
   ```

2. **Installer les dépendances**
   Assurez-vous d'avoir Python 3.8+ installé.
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python main.py
   ```

   Accédez à l'API via `http://127.0.0.1:5000`.

---

## Endpoints API

### Créer une nouvelle transaction
- **URL** : `/transaction/new`
- **Méthode** : POST
- **Données attendues** :
  ```json
  {
      "sender": "adresse_sender",
      "receiver": "adresse_receiver",
      "amount": 100
  }
  ```

### Miner un nouveau bloc
- **URL** : `/mine`
- **Méthode** : GET

### Consulter la blockchain
- **URL** : `/chain`
- **Méthode** : GET

### Résoudre les conflits
- **URL** : `/nodes/resolve`
- **Méthode** : GET

---

## Contract Address

L'adresse du contrat associée à Raficoin Network est :
`0x90efcfac0a160b513c420370b2553c8004b1dc28`

---

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request pour toute suggestion ou correction.

---

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

