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
    data = select_tariftabelle(year, TaxType.EINKOMMEN, tarif)
    first_bracket = data.iloc[0]
    if income <= first_bracket.iloc[0]:
        return 0
    
    current_bracket = first_bracket
    for bracket in data.itertuples():
        if income < bracket[1]:
            break
        else:
            current_bracket = bracket
    return current_bracket[2] + (income - current_bracket[1]) / 100 * current_bracket[3]

def calculate_wealth_tax(year, tarif: Tarif, wealth):
    data = select_tariftabelle(year, TaxType.VERMOEGEN, tarif)
    first_bracket = data.iloc[0]
    if wealth <= first_bracket.iloc[0]:
        return 0
    current_bracket = first_bracket
    for bracket in data.itertuples():
        if wealth < bracket[1]:
            break
        else:
            current_bracket = bracket
    return current_bracket[2] + (wealth - current_bracket[1]) / 1000 * current_bracket[3]
    

income = 100_000
wealth = 385_000

income_tax_grundtarif = calculate_income_tax(2018, Tarif.GRUNDTARIF, income)
income_tax_verheiratetentarif = calculate_income_tax(2018, Tarif.VERHEIRATETENTARIF, income)
wealth_tax_grundtarif = calculate_wealth_tax(2018, Tarif.GRUNDTARIF, wealth)
wealth_tax_verheiratetentarif = calculate_wealth_tax(2018, Tarif.VERHEIRATETENTARIF, wealth)

print("Einkommen: ", income)
print("Vermögen: ", wealth)
print("")
print("== Einfache Steuer == ")
print("Einkommen GT: ", income_tax_grundtarif)
print("Einkommen VT: ", income_tax_verheiratetentarif)
print("Vermögen GT:  ", wealth_tax_grundtarif)
print("Vermögen VT:  ", wealth_tax_verheiratetentarif)