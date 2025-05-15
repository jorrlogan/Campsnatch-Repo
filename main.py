from fastapi import Depends, FastAPI
from auth import verify_clerk_token
from service import Service
from typing import List
from pydantic import BaseModel
from fastapi import Depends

app = FastAPI()
service = Service()


class TrackerRequest(BaseModel):
    userId: str
    deviceToken: str
    facilityId: str
    facilityName: str
    startDate: str
    endDate: str


@app.get("/trackers")
def get_trackers(user_id: str, session=Depends(verify_clerk_token)):
    return service.trackers(user_id)


@app.post("/tracker")
def create_tracker(data: TrackerRequest, session=Depends(verify_clerk_token)):
    return service.create_tracker(
        data.userId,
        data.deviceToken,
        data.facilityId,
        data.facilityName,
        data.startDate,
        data.endDate,
    )


@app.delete("/trackers/{tracker_id}")
def delete_tracker(tracker_id: int, user_id: str, session=Depends(verify_clerk_token)):
    return service.delete_tracker(tracker_id, user_id)


@app.get("/facilities/{search_string}")
def get_facilities(search_string: str, session=Depends(verify_clerk_token)):
    return service.get_facilities(search_string)


@app.get("/facilities/{facility_id}/availability")
def get_facility_availability(facility_id: str, session=Depends(verify_clerk_token)):
    return service.get_facility_availability(facility_id)
