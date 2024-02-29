import pycountry
from data import load_demographic_indicators

# Charger les données
df = load_demographic_indicators()

# Créer un dictionnaire qui associe chaque nom de pays à son code ISO
country_mapping = {country.name: country.alpha_3 for country in pycountry.countries}

# Créer une nouvelle colonne "ISO_code" en mappant les valeurs de la colonne "Location"
# à leurs codes ISO correspondants à l'aide du dictionnaire "country_mapping"
df["ISO_code"] = df["Location"].map(country_mapping)

# Écrire le résultat dans un nouveau fichier CSV
df.to_csv("data/demographic_indicators_with_iso_code.csv", index=False)
