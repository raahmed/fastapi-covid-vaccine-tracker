from fastapi import FastAPI
from datawork import getCountryVaccineCounts, getCountryVaccinePercentages
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

import json

app = FastAPI()

@app.get("/")
async def root():
    data = getCountryVaccineCounts()
    return data

@app.get("/getpercentages")
async def root():
    data = getCountryVaccinePercentages()
    return data

@app.get("/mostpopular")
async def root():
    data = getCountryVaccinePercentages()
    countries = data.keys()
    top_vaccine_by_country = dict()
    for country in countries:
        top_vaccine = ""
        top_vaccine_percentage = 0
        vaccine_names = data[country].keys()
        for vaccine in vaccine_names:
            vaccine_percentage = float(data[country][vaccine])
            if vaccine_percentage > top_vaccine_percentage:
                top_vaccine_percentage = vaccine_percentage
                top_vaccine = vaccine
        top_vaccine_by_country[country] = top_vaccine
    return JSONResponse(top_vaccine_by_country)   

@app.get("/leastpopular")
async def root():
    data = getCountryVaccinePercentages()
    countries = data.keys()
    top_vaccine_by_country = dict()
    for country in countries:
        bottom_vaccine = ""
        bottom_vaccine_percentage = 100
        vaccine_names = data[country].keys()
        for vaccine in vaccine_names:
            vaccine_percentage = float(data[country][vaccine])
            if vaccine_percentage < bottom_vaccine_percentage:
                bottom_vaccine_percentage = vaccine_percentage
                bottom_vaccine = vaccine
        top_vaccine_by_country[country] = bottom_vaccine
    return JSONResponse(top_vaccine_by_country)   
