import os
from dotenv import load_dotenv
import requests
from db import Facility
from peewee import *
import time

load_dotenv()

REC_GOV_API_KEY = os.getenv("REC_GOV_API_KEY")


def get_facilities():
    base_url = "https://ridb.recreation.gov/api/v1/facilities"
    offset = 0
    limit = 50
    while True:
        facilities = requests.get(
            base_url,
            params={"limit": limit, "offset": offset, "apikey": REC_GOV_API_KEY},
        ).json()["RECDATA"]
        if len(facilities) == 0:
            break
        for facility in facilities:
            upsert_facility(facility)
        offset += limit
        time.sleep(0.3)


def upsert_facility(facility_data):
    Facility.insert(
        source_id=facility_data["FacilityID"],
        name=facility_data["FacilityName"],
        description=facility_data["FacilityDescription"],
        reservable=facility_data["Reservable"] == "true",
    ).on_conflict(
        conflict_target=[Facility.source_id],  # Assuming source_id is unique
        preserve=[Facility.name, Facility.description, Facility.reservable],
    ).execute()
    
    
    # class Facility(Model):
    # id = AutoField()
    # source_id = TextField(null=True, unique=True)
    # name = TextField(null=True)
    # location = TextField(null=True)
    # description = TextField(null=True)
    # reservable = BooleanField(null=True)



if __name__ == "__main__":
    get_facilities()
