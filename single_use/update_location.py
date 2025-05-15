import os
from dotenv import load_dotenv
import requests
from db import Facility
from peewee import *
import time
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

REC_GOV_API_KEY = os.getenv("REC_GOV_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


class FacilityLocation(BaseModel):
    name: str
    location: str


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
            print(facility)
        offset += limit
        time.sleep(0.3)


def upsert_facility(facility_data):
    # Extract latitude and longitude
    latitude = facility_data.get("FacilityLatitude")
    longitude = facility_data.get("FacilityLongitude")

    # Extract other relevant fields
    directions = facility_data.get("FacilityDirections", "")
    type_description = facility_data.get("FacilityTypeDescription", "")

    # Prepare input for OpenAI
    facility_name = facility_data["FacilityName"]
    facility_description = facility_data["FacilityDescription"]

    # Send request to OpenAI
    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
            {
                "role": "system",
                "content": "Extract the location description given the campground and location information.",
            },
            {
                "role": "user",
                "content": f"Given the name of this campground: {facility_name} where is it located? latitude: {latitude} longitude: {longitude}, directions: {directions}, type: {type_description}. This is an example of what I want: (Devils Garden campground -> Arches National Park, UT"
            },
        ],
        text_format=FacilityLocation,
    )

    # Use the response to update the location
    location = response.output_parsed.location

    # Insert or update the facility in the database
    Facility.insert(
        source_id=facility_data["FacilityID"],
        name=facility_name,
        location=location,
        description=facility_description,
        reservable=facility_data["Reservable"] == "true",
    ).on_conflict(
        conflict_target=[Facility.source_id],  # Assuming source_id is unique
        preserve=[
            Facility.name,
            Facility.description,
            Facility.reservable,
            Facility.location,
        ],
    ).execute()


if __name__ == "__main__":
    get_facilities()
