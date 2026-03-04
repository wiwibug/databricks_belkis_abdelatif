import re
import bs4
import requests
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
from selenium.webdriver.edge.options import Options
from tqdm import tqdm
import time
import webdriver_manager.chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


edge_options = Options()
edge_options.add_argument("--headless")  # Lancer Edge sans interface graphique
edge_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU pour éviter les erreurs
edge_options.add_argument("--no-sandbox") 

chrome_options = Options()
chrome_options.add_argument("--headless")  # Lancer Chrome sans interface graphique
chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU pour éviter les erreurs
chrome_options.add_argument("--no-sandbox")



# data = {
#     'nom_commercial': [],
#     'classe_therapeutique': [],
#     'dci': [],
#     'indication': [],
#     'age': [],
#     'sexe': [],
#     'date_avis': [],
#     'avis': [],
#     'efficacite': [],
#     'effets_secondaires': []
# }
data = {
    'date' : [],
    'sexe' : [],
    'age' : [],
    'medicament' : [],
    'indications' : [],
    'efficacite' : [],
    'effets_secondaires' : [],
    'avis' : [],
    'url'  : []
    }
# # Initialiser les listes pour stocker les données

date = []
sexe = []
age = []
medicament = []
probleme = []
efficacite = []
effets_secondaires = []
avis = []
url_in = []


# import the urls
urls_brute = pd.read_csv('./url/functional_links.csv', sep=',')
urls = urls_brute['liens_urls']
urls = urls[8001::]
# print(urls)

with tqdm(total=len(urls), desc="Vérification des liens", unit=" lien") as pbar:
    
    for url in urls:
    # def get_soup(url):
        
        
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Edge(options=edge_options)
        driver.get(url)
        url_in = url
        match = re.search(r'/www.meamedica.fr/([^/]+)/', url)
        for index, row in urls_brute.iterrows():
            url = row['liens_urls']
        pbar.update(1) # Mise à jour de la progression
        if match:
            classes_therapeutiques= match.group(1)
        
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser',)
        elements = soup.find_all('div', class_="vote rounded btn-left")
        for element in elements:
            text = element.find_all('div', class_="subText")
            review = element.find_all('div', class_="review")
            rating = element.find_all('div', class_="ratings")
        
            for rate in rating:
                
                labels = rate.find_all("span")
                
                for label in labels:
                    if label.has_attr("title"):
                        if "efficace" in label["title"]:
                            efficacite = label["title"]
                            
                        else:
                            
                            effets_secondaires = label["title"]
            for r in review:
                avis = r.find('span').get_text()
                
            for t in text:
                ecrit  = t.get_text()
                date_sexe_age_pattern = r"(\d{2}/\d{2}/\d{4}) \| ([^|]+) \| (\d+)"
                date_sexe_age_match = re.search(date_sexe_age_pattern, ecrit)
                lignes = ecrit.strip().split('\n')
                
                
                if date_sexe_age_match:
                    
                    date = date_sexe_age_match.group(1)
                    
                    sexe = date_sexe_age_match.group(2).strip()
                    
                    age = date_sexe_age_match.group(3)
                    

                if len(lignes) >= 4:  # Vérifier qu'on a assez de lignes pour extraire les infos
                    medicament = lignes[2].strip()
                    probleme = lignes[3].strip()
                   
                medicament = medicament
                probleme = probleme

                # Ajouter les valeurs aux listes dans le dictionnaire data
                data['date'].append(date)
                data['sexe'].append(sexe)
                data['age'].append(age)
                data['medicament'].append(medicament)
                data['indications'].append(probleme)
                data['efficacite'].append(efficacite)
                data['effets_secondaires'].append(effets_secondaires)
                data['avis'].append(avis)
                data['url'].append(url_in)
       
# Création du DataFrame
# df = pd.DataFrame(data)
# df.to_csv('resultats_9000.csv', index=False, encoding='utf-8', sep=',')

