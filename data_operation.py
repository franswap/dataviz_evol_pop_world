import pandas as pd
import pycountry

# Charger les données depuis un fichier CSV
df = pd.read_csv(
    "data/data1.csv",
    dtype={
        "SortOrder": int,
        "LocID": int,
        "Notes": str,
        "ISO3_code": str,
        "ISO2_code": str,
        "SDMX_code": str,
        "LocTypeID": int,
        "LocTypeName": str,
        "ParentID": int,
        "Location": str,
        "VarID": int,
        "Variant": str,
        "Time": int,
        "TPopulation1Jan": float,
        "TPopulation1July": float,
        "TPopulationMale1July": float,
        "TPopulationFemale1July": float,
        "PopDensity": float,
        "PopSexRatio": float,
        "MedianAgePop": float,
        "NatChange": float,
        "NatChangeRT": float,
        "PopChange": float,
        "PopGrowthRate": float,
        "DoublingTime": float,
        "Births": float,
        "Births1519": float,
        "CBR": float,
        "TFR": float,
        "NRR": float,
        "MAC": float,
        "SRB": float,
        "Deaths": float,
        "DeathsMale": float,
        "DeathsFemale": float,
        "CDR": float,
        "LEx": float,
        "LExMale": float,
        "LExFemale": float,
        "LE15": float,
        "LE15Male": float,
        "LE15Female": float,
        "LE65": float,
        "LE65Male": float,
        "LE65Female": float,
        "LE80": float,
        "LE80Male": float,
        "LE80Female": float,
        "InfantDeaths": float,
        "IMR": float,
        "LBsurvivingAge1": float,
        "Under5Deaths": float,
        "Q5": float,
        "Q0040": float,
        "Q0040Male": float,
        "Q0040Female": float,
        "Q0060": float,
        "Q0060Male": float,
        "Q0060Female": float,
        "Q1550": float,
        "Q1550Male": float,
        "Q1550Female": float,
        "Q1560": float,
        "Q1560Male": float,
        "Q1560Female": float,
        "NetMigrations": float,
        "CNMR": float,
    },
)

# Créer un dictionnaire qui associe chaque nom de pays à son code ISO
country_mapping = {country.name: country.alpha_3 for country in pycountry.countries}

# Créer une nouvelle colonne "ISO_code" en mappant les valeurs de la colonne "Location"
# à leurs codes ISO correspondants à l'aide du dictionnaire "country_mapping"
df["ISO_code"] = df["Location"].map(country_mapping)

# Écrire le résultat dans un nouveau fichier CSV
df.to_csv("data/data1_with_iso.csv", index=False)
