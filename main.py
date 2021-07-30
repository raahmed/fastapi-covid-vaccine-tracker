from typing import Dict
from fastapi import FastAPI
import json
from starlette.responses import JSONResponse
from models import CountryVaccineSummary
from datawork import get_country_vaccine_percentages
import json
import typing

from starlette.responses import Response

class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
            sort_keys=True,
        ).encode("utf-8")

app = FastAPI()

@app.get("/", response_class=PrettyJSONResponse)
async def root():
    data = get_country_vaccine_percentages()
    return data


@app.get("/data", response_class=PrettyJSONResponse)
async def root():
    data = get_country_vaccine_percentages()
    return data

@app.get("/mostcommon", response_class=PrettyJSONResponse)
async def most_common() -> Dict[str, str]:
    data = get_country_vaccine_percentages()
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

@app.get("/leastcommon", response_class=PrettyJSONResponse)
async def least_common() -> Dict[str, str]:
    data = get_country_vaccine_percentages()
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
