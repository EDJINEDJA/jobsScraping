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

    def __len__(self, responses):
        return len(responses)

   
    def scraping(self):
        #Initialization
        client = Api(client_id=os.getenv("CLIENT_ID"), 
                    client_secret=os.getenv("CLIENT_SECRET"))

        start_dt = datetime.datetime(self.config["START_YEAR"], self.config["START_MONTH"] , self.config["START_DAY"], self.config["START_HOURS"], self.config["START_MIN"])
        end_dt = datetime.datetime.today()
        
        params = {

            "motsCles": self.config["KEYWORDS"],
            'minCreationDate': dt_to_str_iso(start_dt),
            'maxCreationDate': dt_to_str_iso(end_dt)
        }

        search_on_jobs = client.search(params=params)

        return search_on_jobs["resultats"]

    def make_csv(self):
        jobs = self.scraping()
        
        if not os.path.exists(self.config["OUTPUTPATH"]+ "jobs.csv"):
            # Ouverture du fichier en mode 'append' pour ajouter de nouvelles lignes
            with open(self.config["OUTPUTPATH"]+ "jobs.csv", mode='a', newline='', encoding="utf-8") as file:
                # Définition des colonnes dans un objet DictWriter
                writer = csv.DictWriter(file, fieldnames=["Index","date Creation","date Actualisation","Offres d'emploi","Missions","Compétences","Qualifications Pro","Types de contrat","Lieu de travail","Entreprise","Qualifications"])

                # Écriture de l'en-tête
                writer.writeheader()

        for idx in range(self.__len__(jobs)):
            Index = idx
            dateCR=jobs[idx]['dateCreation']
            dateAct=jobs[idx]['dateActualisation']
            Offre = jobs[idx]['intitule']
            Missions = jobs[idx]['description']
            try: 
                Compétences = jobs[idx]['competences']
                QualificationsPro = jobs[idx]["qualitesProfessionnelles"]
            except KeyError:
                Compétences = " "
                QualificationsPro = " "

            Lieu = jobs[idx]['lieuTravail']
            Contrat = jobs[idx]['typeContrat']
            Entreprise = jobs[idx]['entreprise']
            Qualifications = jobs[idx]['qualificationLibelle']

            row = [Index,dateCR,dateAct, Offre , Missions , Compétences, QualificationsPro ,Contrat , Lieu , Entreprise , Qualifications]
            
            # Ouverture du fichier en mode 'append' pour ajouter de nouvelles lignes
            with open(self.config["OUTPUTPATH"]+ "jobs.csv", mode='a', newline='', encoding="utf-8") as file1:
                writer1 = csv.writer(file1)
                # Écriture d'une nouvelle ligne dans le fichier CSV
                writer1.writerow(row)
            time.sleep(1)

        print("done °°°°°")