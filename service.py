from db import Tracker
from playhouse.shortcuts import model_to_dict
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from rec_gov_api import get_facility_availability as get_rec_gov_availability
from db import Facility


class Service:
    def trackers(self, user_id: str):
        trackers = Tracker.select().where(Tracker.user_id == user_id)
        return [model_to_dict(tracker) for tracker in trackers]

    def create_tracker(
        self,
        user_id: str,
        device_token: str,
        facility_id: str,
        facility_name: str,
        start_date: str,
        end_date: str,
    ):
        Tracker.create(
            user_id=user_id,
            device_token=device_token,
            facility_id=facility_id,
            facility_name=facility_name,
            start_date=start_date,
            end_date=end_date,
        )
        trackers = Tracker.select().where(Tracker.user_id == user_id)
        return [model_to_dict(tracker) for tracker in trackers]

    def delete_tracker(self, tracker_id: int, user_id: str):
        tracker = Tracker.get(Tracker.id == tracker_id, Tracker.user_id == user_id)
        tracker.delete_instance()
        return {"message": "Tracker deleted successfully"}

    def get_facilities(self, search_string: str):
        facilities = Facility.select().where(Facility.name.contains(search_string))
        return [model_to_dict(facility) for facility in facilities]

    def get_facility_availability(self, facility_id: str):
        print(f"Getting availability for facility: {facility_id}")

        # Get today's date
        today = date.today()
        print(f"Today's date: {today}")

        # Get first day of current month
        first_day_current = date(today.year, today.month, 1)
        print(f"First day of current month: {first_day_current}")

        # Get first day of next two months
        first_day_next = first_day_current + relativedelta(months=1)
        first_day_next_next = first_day_current + relativedelta(months=2)
        print(f"First day of next month: {first_day_next}")
        print(f"First day of next next month: {first_day_next_next}")

        # Get availability for each month
        print("Fetching current month availability...")
        current_month = get_rec_gov_availability(
            facility_id, first_day_current.isoformat()
        )
        print(f"Current month data points: {len(current_month)}")

        print("Fetching next month availability...")
        next_month = get_rec_gov_availability(facility_id, first_day_next.isoformat())
        print(f"Next month data points: {len(next_month)}")

        print("Fetching next next month availability...")
        next_next_month = get_rec_gov_availability(
            facility_id, first_day_next_next.isoformat()
        )
        print(f"Next next month data points: {len(next_next_month)}")

        # Combine all availability data
        combined_availability = [
            {"date": date, "is_available": available}
            for date, available in {
                **current_month,
                **next_month,
                **next_next_month,
            }.items()
        ]
        print(f"Total combined data points: {len(combined_availability)}")

        return combined_availability


if __name__ == "__main__":
    service = Service()
    print(service.get_facility_availability("234059"))
