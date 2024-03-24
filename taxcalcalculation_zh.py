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
    
def calculate_income_tax(year, tarif: Tarif, income):
    # Select the tax table
    data = select_tariftabelle(year, TaxType.EINKOMMEN, tarif)
    # select first entry
    first_bracket = data.iloc[0]
    if income <= first_bracket[1]:
        return 0
    
    current_bracket = first_bracket
    for bracket in data.itertuples():
        if income < bracket[1]:
            break
        else:
            current_bracket = bracket
    return current_bracket[2] + (income - current_bracket[1]) / 100 * current_bracket[3]
    

income = 100_000
income_tax_grundtarif = calculate_income_tax(2018, Tarif.GRUNDTARIF, income)
income_tax_verheiratetentarif = calculate_income_tax(2018, Tarif.VERHEIRATETENTARIF, income)

print("einfache steuer einkommen grundtarif:           ", income_tax_grundtarif)
print("einfache steuer einkommen verheiratetentarif:   ", income_tax_verheiratetentarif)



# data = select_tariftabelle(
#     year = 2018, 
#     tax_type = TaxType.EINKOMMEN,
#     tarif =Tarif.VERHEIRATETENTARIF,
# )
# print(data)