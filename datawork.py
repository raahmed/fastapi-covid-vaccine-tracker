import os
import psycopg2
import json
from models import CountryVaccineSummary, CountryVaccineData


VACCINE_TYPE = { "COM": "Pfizer/BioNTech", \
    "MOD": "Moderna", \
    "CN": "SinoPharm",\
    "SIN": "Coronavac – Sinovac", \
    "JANSS": "J&J Janssen", \
    "SPU": "Sputnik V",\
    "AZ": "AstraZeneca", \
    "UNK": "Unknown" }

COUNTRY_CODES = {
    "BE": "Belgium",\
    "BG": "Bulgaria",\
    "CZ": "Czechia",\
    "FR": "France",\
    "DK": "Denmark",\
    "DE": "Germany",\
    "EE": "Estonia",\
    "IE": "Ireland",\
    "EL": "Greece",\
    "ES": "Spain",\
    "HR": "Croatia",\
    "IT": "Italy",\
    "CY": "Cypress",\
    "LV": "Latvia",\
    "LT": "Lithuania",\
    "LU": "Luxembourg",\
    "HU": "Hungary",\
    "MT": "Malta",\
    "NL": "Netherlands",\
    "AT": "Austria",\
    "PL": "Poland",\
    "PT": "Portugal",\
    "RO": "Romania",\
    "SI": "Slovenia",\
    "SK":"Slovakia",\
    "FI": "Finland",\
    "SE": "Sweden",\
    "IS": "Iceland",\
    "LI": "Leichtenstein",\
    "CH": "Switzerland",\
    "NO": "Norway",\
    "UK": "United Kingdom"
    }

def write_config(conn_string):
    with open(".conninfo","w") as source:
        source.write(conn_string)
        return "Successfully wrote config file"


def connect():
    connection_string=os.getenv("CONNECTION_STRING")
    try:
        conn=psycopg2.connect(connection_string)
        return conn
    except:
        print("Database connection error: \
            Is your connection string set properly in Configuration Settings?")
        return None

def load_data(filename="covid_data.csv"):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    cursor.execute('DROP TABLE IF EXISTS vaccine_data')    
    cursor.execute('CREATE TABLE vaccine_data(NumberDosesReceived bigint,\
        ReportingCountry text, Vaccine text);')

    conn.commit()
    with open(filename,'r') as incoming:
        cursor.copy_expert('COPY raw_data FROM stdin CSV',incoming)
        
        #Add data to database
        cursor.execute('INSERT INTO vaccine_data SELECT SUM(NumberDosesReceived),\
            ReportingCountry,Vaccine FROM raw_data GROUP BY reportingcountry, vaccine')

        conn.commit()
        return "Data loaded successfully"

def get_all_data():
    ret=dict()
    conn=connect()
    cursor=conn.cursor()
    
    #Retrieves all the data
    cursor.execute('SELECT * FROM vaccine_data')

    for entry in cursor.fetchall():
        print(entry)
    return None

def get_country_vaccine_percentages() -> CountryVaccineSummary:
    vaccine_dose_counts: CountryVaccineSummary = get_country_vaccine_counts()
    for country in vaccine_dose_counts.country_names():
        total_doses = vaccine_dose_counts.country_data[country].total_doses
        if total_doses == 0:
            continue
        for vaccine_type in vaccine_dose_counts.country_data[country].vaccine_types():
            percentage = (vaccine_dose_counts.country_data[country].vaccine_stats[vaccine_type] / total_doses) * 100
            percentage = round(percentage,2)
            vaccine_dose_counts.country_data[country].vaccine_stats[vaccine_type] = percentage
    return vaccine_dose_counts

def get_country_vaccine_counts() -> CountryVaccineSummary:
    summary_information: CountryVaccineSummary = CountryVaccineSummary()
    conn=connect()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM vaccine_data')
    conn.commit()
    for entry in cursor.fetchall():
        doses, country, vaccine_type=entry
        country = COUNTRY_CODES.get(country, country)
        vaccine_type =  VACCINE_TYPE.get(vaccine_type, vaccine_type)
        if doses is None:
            doses = 0
        if country not in summary_information.country_data:
            summary_information.country_data[country] = CountryVaccineData(total_doses=0)

        if vaccine_type not in summary_information.country_names():
            summary_information.country_data[country].vaccine_stats[vaccine_type] = doses
            summary_information.country_data[country].total_doses += doses
        else:
            try:
                summary_information.country_data[country].vaccine_stats[vaccine_type] += int(doses)
                summary_information.country_data[country].total_doses += doses
            except:
                print("An error occurred")
                print(doses, country, vaccine_type)
    return summary_information


def print_get_country_vaccine_percentages():
    return get_country_vaccine_percentages().json()


def print_get_country_vaccine_counts():
    return get_country_vaccine_counts().json()


if __name__ == '__main__':
    import fire
    fire.Fire({"writeConfig":write_config,\
    "loadData":load_data,\
    "getAllData": get_all_data,\
    "getCountryVaccineCounts": print_get_country_vaccine_counts,\
    "getCountryVaccinePercentages": print_get_country_vaccine_percentages})
