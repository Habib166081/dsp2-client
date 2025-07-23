"""
full_report.py

Ce script génère automatiquement un fichier .json pour chaque utilisateur DSP2 (ex : Maurice, Antoinette),
contenant toute l’identité, les comptes, soldes et **toutes les transactions** (pagination incluse).
Les fichiers sont créés dans le dossier 'examples/reports/'.

Usage :
    python examples/full_report.py

Résultat :
    - report_mdupuis.json
    - report_agribard.json
dans /examples/reports/
"""

import json
from pathlib import Path
from dsp2_client.core.client import DSP2Client

USERS = [
    {"username": "mdupuis", "password": "111111", "display": "Maurice Dupuis"},
    {"username": "agribard", "password": "222222", "display": "Antoinette Gribard"},
]

REPORT_DIR = Path(__file__).parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def to_json_serializable(obj):
    """Convertit récursivement tous les objets datetime en chaîne ISO pour l'export JSON."""
    if isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_serializable(i) for i in obj]
    elif hasattr(obj, "isoformat"):
        return obj.isoformat()
    return obj

def fetch_all_transactions(client, account_id, page_size=50):
    """Récupère toutes les transactions pour un compte via pagination complète."""
    all_tx = []
    page = 1
    while True:
        txs = client.list_transactions(account_id, page=page, count=page_size)
        if not txs:
            break
        all_tx.extend([t.model_dump() for t in txs])
        if len(txs) < page_size:
            break
        page += 1
    return all_tx

def generate_report(user_info):
    username, password, display = user_info["username"], user_info["password"], user_info["display"]
    report = {
        "identity": None,
        "accounts": [],
    }
    with DSP2Client(username=username, password=password) as client:
        identity = client.get_identity()
        report["identity"] = identity.model_dump()

        accounts = client.list_accounts()
        for acc in accounts:
            acc_dict = acc.model_dump()
            acc_dict["balances"] = [bal.model_dump() for bal in client.list_balances(acc.id)]
            acc_dict["transactions"] = fetch_all_transactions(client, acc.id)
            report["accounts"].append(acc_dict)

    # Convert datetime to isoformat for JSON serialization
    report_serializable = to_json_serializable(report)
    file_name = f"report_{username}.json"
    file_path = REPORT_DIR / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_serializable, f, indent=2, ensure_ascii=False)
    print(f"[OK] Fichier généré pour {display}: {file_path}")

if __name__ == "__main__":
    print("\nCe script va générer un fichier .json pour chaque utilisateur DSP2,")
    print(f"et enregistrer les rapports dans le dossier '{REPORT_DIR.relative_to(Path.cwd())}'.\n")
    for user in USERS:
        generate_report(user)
    print("\n✅ Tous les fichiers ont été générés dans le dossier 'examples/reports'.")
