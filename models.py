from pydantic import BaseModel
from typing import Dict, KeysView


class CountryVaccineData(BaseModel):
    vaccine_stats: Dict[str, float] = {}
    total_doses: int = 0
    
    def vaccine_types(self) -> KeysView[str]:
        return self.vaccine_stats.keys()


class CountryVaccineSummary(BaseModel):
    country_data: Dict[str, CountryVaccineData] = {}

    def country_names(self) -> KeysView[str]:
        return self.country_data.keys()
