import pandas as pd
from enum import Enum

class TaxType(Enum):
    EINKOMMEN = 1
    VERMOEGEN = 2
    
class Tarif(Enum):
    GRUNDTARIF = 1
    VERHEIRATETENTARIF = 2


def select_tariftabelle(year, tax_type: TaxType, tarif: Tarif):
    # Construct the filename
    filename = f"./tariftabellen/{year}-{tax_type.name.lower()}-{tarif.name.lower()}.csv"
    names_einkommen = ['Einkommensbereich (CHF)', 'Steuer Grundtarif (CHF)', 'Zusätzlicher Steuerbetrag pro 100 CHF']
    names_vermoegen = ['steuerbares Vermögen (CHF)', 'Steuer (CHF)', 'für je weitere 1000. Vemögen']
    names = names_einkommen if tax_type == 'einkommen' else names_vermoegen
    # Read the CSV file
    try:
        data = pd.read_csv(filename, names=names, skiprows=1, header=None)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found. Please check the file path.")
        return None

data = select_tariftabelle(
    year = 2018, 
    tax_type = TaxType.EINKOMMEN,
    tarif =Tarif.VERHEIRATETENTARIF,
)
print(data)