import pandas as pd
from enum import Enum

class TaxType(Enum):
    EINKOMMEN = 1
    VERMOEGEN = 2

class Tarif(Enum):
    GRUNDTARIF = 1
    VERHEIRATETENTARIF = 2


def select_tariftabelle(year, tax_type: TaxType, tarif: Tarif):
    filename = f"./tariftabellen/{year}-{tax_type.name.lower()}-{tarif.name.lower()}.csv"
    names_einkommen = ['Einkommensbereich (CHF)', 'Steuer Grundtarif (CHF)', 'Zusätzlicher Steuerbetrag pro 100 CHF']
    names_vermoegen = ['steuerbares Vermögen (CHF)', 'Steuer (CHF)', 'für je weitere 1000. Vemögen']
    names = names_einkommen if tax_type == 'einkommen' else names_vermoegen
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

def calculate_staats_gemeinde_steuern(year, tarif: Tarif, income, wealth):
    income_tax = calculate_income_tax(year, tarif, income)
    wealth_tax = calculate_wealth_tax(year, tarif, wealth)
    staatssteuerfuss = 0.99
    gemeindesteuerfuss = 1.19
    return income_tax * staatssteuerfuss + income_tax * gemeindesteuerfuss + wealth_tax * staatssteuerfuss + wealth_tax * gemeindesteuerfuss
    

income = 68_900
wealth = 159_000

income_tax_grundtarif = calculate_income_tax(2018, Tarif.GRUNDTARIF, income)
income_tax_verheiratetentarif = calculate_income_tax(2018, Tarif.VERHEIRATETENTARIF, income)
wealth_tax_grundtarif = calculate_wealth_tax(2018, Tarif.GRUNDTARIF, wealth)
wealth_tax_verheiratetentarif = calculate_wealth_tax(2018, Tarif.VERHEIRATETENTARIF, wealth)

staats_gemeinde_steuern_grundtarif = calculate_staats_gemeinde_steuern(2018, Tarif.GRUNDTARIF, income, wealth)
staats_gemeinde_steuern_verheiratetentarif = calculate_staats_gemeinde_steuern(2018, Tarif.VERHEIRATETENTARIF, income, wealth)


print("Einkommen: ", "{:,.2f}".format(income))
print("Vermögen: ", "{:,.2f}".format(wealth))
print("")
print("== Einfache Steuer == ")
print("Einkommen GT: ", "{:,.2f}".format(income_tax_grundtarif))
print("Einkommen VT: ", "{:,.2f}".format(income_tax_verheiratetentarif))
print("Vermögen GT:  ", "{:,.2f}".format(wealth_tax_grundtarif))
print("Vermögen VT:  ", "{:,.2f}".format(wealth_tax_verheiratetentarif))
print("")
print("== Staats- und Gemeindesteuern ==")
print("Einkommen GT: ", "{:,.2f}".format(staats_gemeinde_steuern_grundtarif))
print("Einkommen VT: ", "{:,.2f}".format(staats_gemeinde_steuern_verheiratetentarif))
