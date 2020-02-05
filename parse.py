### Permet d'extraire liste des hotels a moins de 70e la nuit et plus de 500 avis
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

def main():
    download = False
    if download:
        url = 'https://www.tripadvisor.fr/Hotels-g187497-Barcelona_Catalonia-Hotels.html'
        # Telecharge le contenu du fichier html
        response = urllib.request.urlopen(url)
        webContent = response.read().decode("utf-8")
        # On peut sauvegarde dans un fichier
        with open('webpage.html', 'w') as f:
            f.write(webContent)
    else:
        # Pour éviter de re-télécharger:
        with open('webpage.html', 'r') as f:
            webContent = f.read()


    # On parse le html
    soup = BeautifulSoup(webContent, 'html.parser')

    # sous forme de liste d'éléments: liste de tous les hôtels (blocs principaux de la page web)
    boxes = soup.find_all("div", {"class": "listItem"})
    # print(f"J'ai trouvé {len(boxes)} conteneurs d'un élément de liste")

    infos = list() # liste de listes
    # Pour chaque hotel de la liste des hôtels
    for box in boxes:
        # Dans le container, cherche les avis
        nbAvis, prix, nom = extractData(box)

        if prix is not None:
            infos_box = [nom, nbAvis, prix]
            infos.append(infos_box)

    # infos a toutes les infos, on trie et affiche:
    postProcessing(infos)



def postProcessing(infos):
    db = pd.DataFrame(infos, columns=['Nom','Avis','Prix'])
    # Critères
    print("** Filtre: la liste des hotels a moins de 70e la nuit et plus de 500 avis **")
    filtered = db.loc[(db['Prix']<70) & (db['Avis']>500),:]
    for index, row in filtered.iterrows():
        print(f"-> {row['Nom']}: {row['Prix']}e, {row['Avis']} avis")



def extractData(box):
    review_container = box.find("a", {"class": "review_count"})
    str_avis = review_container.string # 1 013 avis
    str_avis = str_avis[:-5] # 1 013: on retire les 5 derniers caractères
    nbAvis = int(str_avis.replace('\xa0','')) # 1013: on retire les espaces (\xa0)
    # print(f"L'hotel a {nbAvis} avis")

    # Et les prix
    price_container = box.find("div", {"class": "price"})
    str_price = price_container.string # 79€
    prix = None
    if str_price is not None:
        str_price = str_price[:-1] # 79
        prix = int(str_price)
    # print(f"La nuit coûte {prix} euros")

    # Et le nom (par le container parent)
    title = box.find('div', {'class': 'listing_title'}).findChild("a" , recursive=False)
    nomHotel = title.string

    return nbAvis, prix, nomHotel



if __name__=='__main__':
    main()
