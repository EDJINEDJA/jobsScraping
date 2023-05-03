from offres_emploi import Api
from dotenv import load_dotenv

from offres_emploi.utils import dt_to_str_iso
import datetime
import os
import csv
import time

load_dotenv("./env/.env")

class Jobs():
    def __init__(self , config) -> None:
        self.config = config
        #Initialization
        self.client = Api(client_id=os.getenv("CLIENT_ID"), 
                    client_secret=os.getenv("CLIENT_SECRET"))
        self.start_dt = datetime.datetime(self.config["START_YEAR"], self.config["START_MONTH"] , self.config["START_DAY"], self.config["START_HOURS"], self.config["START_MIN"])
        self.end_dt = datetime.datetime.today()
        


    def __len__(self, responses):
        return len(responses)

    def lenContent(self):
        params = {

            "motsCles": self.config["KEYWORDS"],
            'minCreationDate': dt_to_str_iso(self.start_dt),
            'maxCreationDate': dt_to_str_iso(self.end_dt)
        }

        search_on_jobs = self.client.search(params=params)
        ContentRange = int(search_on_jobs['Content-Range']['max_results'])
        slice = [idx for idx in range(0,ContentRange,150)]
        range_=[f"{slice[idx]}" +"-"+f"{slice[idx+1]-1}" for idx in range(len(slice)) if idx < len(slice)-1] + [f"{slice[-1]}" +"-"+f"{ContentRange}"]
        return range_

    def scraping(self, item):
        params = {

            "motsCles": self.config["KEYWORDS"],
            'minCreationDate': dt_to_str_iso(self.start_dt),
            'maxCreationDate': dt_to_str_iso(self.end_dt),
            'range': f'{item}'
            }

        search_on_jobs = self.client.search(params=params)
        resultats = search_on_jobs["resultats"]

        return resultats

    def make_csv(self):
        if not os.path.exists(self.config["OUTPUTPATH"]+ "jobs.csv"):
                # Ouverture du fichier en mode 'append' pour ajouter de nouvelles lignes
                with open(self.config["OUTPUTPATH"]+ "jobs.csv", mode='a', newline='', encoding="utf-8") as file:
                    # Définition des colonnes dans un objet DictWriter
                    writer = csv.DictWriter(file, fieldnames=["Index","date Creation","date Actualisation","Offres d'emploi","Missions","Compétences","Qualifications Pro","Types de contrat","Lieu de travail","Entreprise","Qualifications"])
                    # Écriture de l'en-tête
                    writer.writeheader()

        ContentRange = self.lenContent()
        compt = 0
        for item in ContentRange:
            jobs = self.scraping(item)
            for idx in range(self.__len__(jobs)):
                
                Index = compt
                dateCR=jobs[idx]['dateCreation']
                dateAct=jobs[idx]['dateActualisation']
                Offre = jobs[idx]['intitule']
                Missions = jobs[idx]['description']
                try: 
                    Compétences = jobs[idx]['competences']
                    QualificationsPro = jobs[idx]["qualitesProfessionnelles"]
                    Qualifications = jobs[idx]['qualificationLibelle']
                except KeyError:
                    Compétences = " "
                    QualificationsPro = " "
                    Qualifications = " "
                Lieu = jobs[idx]['lieuTravail']
                Contrat = jobs[idx]['typeContrat']
                Entreprise = jobs[idx]['entreprise']

                row = [Index , dateCR, dateAct , Offre , Missions , Compétences, QualificationsPro , Contrat , Lieu , Entreprise , Qualifications]
                
                # Ouverture du fichier en mode 'append' pour ajouter de nouvelles lignes
                with open(self.config["OUTPUTPATH"]+ "jobs.csv", mode='a', newline='', encoding="utf-8") as file1:
                    writer1 = csv.writer(file1)
                    # Écriture d'une nouvelle ligne dans le fichier CSV
                    writer1.writerow(row)
                compt=compt+1
            time.sleep(2)
        print("done °°°°°")