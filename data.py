import pandas as pd


def load_demographic_indicators():
    df = pd.read_csv(
        "data/demographic_indicators.csv",
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

    return df
