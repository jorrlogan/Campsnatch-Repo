import requests
from typing import Dict
from urllib.parse import quote


def get_facility_availability(facility_id: str, start_date: str) -> Dict[str, bool]:
    encoded_date = quote(f"{start_date}T00:00:00.000Z")
    print(f"Fetching availability for date: {encoded_date}")
    url = f"https://www.recreation.gov/api/camps/availability/campground/{facility_id}/month?start_date={encoded_date}"

    print(f"Making request to: {url}")
    response = requests.get(
        url, headers={"accept": "application/json", "User-Agent": "Mozilla/5.0"}
    )

    if not response.ok:
        print(f"Error response from API: {response.status_code} - {response.text}")
        return {}

    json_data = response.json()
    if "campsites" not in json_data:
        print(f"Unexpected API response format: {json_data}")
        return {}

    campsites = json_data["campsites"]
    print(f"Found {len(campsites)} campsites")

    # Create availability map
    availability_map = {}
    for site_id, site_data in campsites.items():
        camp_availability = site_data["availabilities"]
        for day, status in camp_availability.items():
            if day not in availability_map:
                availability_map[day] = []
            availability_map[day].append(status)

    # Create final tally map
    tally_map = {}
    for day, statuses in availability_map.items():
        is_open = any(status == "Available" for status in statuses)
        tally_map[day] = is_open

    print(f"Returning availability for {len(tally_map)} days")
    return tally_map


if __name__ == "__main__":
    print(get_facility_availability("234059", "2025-05-01"))
