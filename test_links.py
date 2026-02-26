import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime

liens = pd.read_csv('./url/csv_url.csv', sep=',', encoding='utf-8')
liens = liens.iloc[1:10]  # garde les lignes 1 à 9

def check_link(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in [200, 403]:
            return "✅ Fonctionnel"
        return f"⚠️ Problème ({response.status_code})"
    except requests.RequestException:
        return "❌ Inaccessible"

results = []
with tqdm(total=len(liens), desc="Vérification des liens", unit=" lien") as pbar:
    for _, row in liens.iterrows():
        url = row['url']
        status = check_link(url)
        tested_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # datetime du test
        results.append((url, status, tested_at))
        pbar.update(1)

df_results = pd.DataFrame(results, columns=["url", "statut", "datetime"])
df_results.to_csv(f'./url/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.csv', index=False, encoding='utf-8')

print(df_results)