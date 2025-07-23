# DSP2 Client SDK

> **SDK Python pro pour consommer l’API DSP2 bancaire**

---

## 🚀 Pourquoi utiliser ce SDK ?

- Plus besoin de manipuler du JSON ou des requêtes HTTP à la main.


---

## 🛠️ Installation & Setup

**1. Cloner le repo et entrer dedans :**
```bash
git clone https://github.com/Habib166081/dsp2-client.git
cd dsp2-client
```

**2. Créer l’environnement virtuel et installer les dépendances :** _(avec `uv`, gestionnaire moderne Python)_
```bash
uv venv
.venv\Scripts\activate  # (Windows)
uv pip install -r requirements.txt
```

**3. (Facultatif mais recommandé) Installer les hooks pre-commit :** _(pour un code toujours propre)_
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

**4. Configurer les variables d’environnement :**

- Copier `.env` et ajuster au besoin.

Exemple `.env` :
```ini
base_url="https://dsp2-technical-test.iliad78.net"
log_level="INFO"
```
---

## 🚦 Lancer les exemples et scripts

**Avant d’exécuter un script dans le dossier `examples/`, installe le projet en mode développement**


```bash
uv pip install -e
python examples/simple_usage.py
```

---

## 📦 Utilisation rapide

```python
from dsp2_client.core.client import DSP2Client

with DSP2Client(username="mdupuis", password="111111") as client:
    identity = client.get_identity()
    print(identity)

    accounts = client.list_accounts()
    for acc in accounts:
        print("Account:", acc)
        balances = client.list_balances(acc.id)
        print("Balances:", balances)
        transactions = client.list_transactions(acc.id, page=1, count=5)
        for tx in transactions:
            print("Transaction:", tx)
```

_Voir aussi : `examples/simple_usage.py`_

---

## 🧩 Structure du projet

```plaintext
src/dsp2_client/
│
├── core/
│   ├── session.py   # Gestion session HTTP, auth, logs, context manager
│   └── client.py    # Point d’entrée principal du SDK (DSP2Client)
│
├── models/
│   ├── identity.py  # Modèles Pydantic ultra-typiés
│   ├── account.py
│   ├── balance.py
│   ├── transaction.py
│   └── common.py
│
├── services/
│   ├── identity.py
│   ├── account.py
│   ├── balance.py
│   └── transaction.py
│
├── config.py        # Configuration centralisée avec Pydantic
├── .env             # fichier d’environnement
```


## ⚡ Bonnes pratiques & Tooling

- **`uv`** : gestionnaire ultra-rapide de dépendances (remplace pip/pipenv/poetry).
- **`pre-commit`** : valide le code avant chaque commit (`ruff`, trailing spaces, etc.).
- **`pytest`, `ruff`, `mypy`** : garantissent une qualité de code pro (cf. `pyproject.toml`).



## 🧪 Tests

Lancer les tests :
```bash
pytest
```

Vérifier le lint et typage :
```bash
ruff check .
mypy src/
```
