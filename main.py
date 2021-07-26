from typing import Dict
from fastapi import FastAPI
from models import CountryVaccineSummary
from datawork import getCountryVaccinePercentages

app = FastAPI()

@app.get("/data", response_model=CountryVaccineSummary)
async def root():
    data = getCountryVaccinePercentages()
    return data

@app.get("/mostpopular")
async def most_popular() -> Dict[str, str]:
    data = getCountryVaccinePercentages()
    top_vaccine_by_country: Dict[str, str] = dict()
    for country in data.country_names():
        top_vaccine = ""
        top_vaccine_percentage = 0
        for vaccine in data.country_data[country].vaccine_types():
            vaccine_percentage = float(data.country_data[country].vaccine_stats[vaccine])
            if vaccine_percentage > top_vaccine_percentage:
                top_vaccine_percentage = vaccine_percentage
                top_vaccine = vaccine
        top_vaccine_by_country[country] = top_vaccine
    return top_vaccine_by_country

@app.get("/leastpopular")
async def least_popular() -> Dict[str, str]:
    data = getCountryVaccinePercentages()
    top_vaccine_by_country: Dict[str, str] = dict()
    for country in data.country_names():
        bottom_vaccine = ""
        bottom_vaccine_percentage = 100
        for vaccine in data.country_data[country].vaccine_types():
            vaccine_percentage = float(data.country_data[country].vaccine_stats[vaccine])
            if vaccine_percentage < bottom_vaccine_percentage:
                bottom_vaccine_percentage = vaccine_percentage
                bottom_vaccine = vaccine
        top_vaccine_by_country[country] = bottom_vaccine
    return top_vaccine_by_country
