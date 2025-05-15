from peewee import *
from playhouse.migrate import SqliteMigrator, migrate
from playhouse.postgres_ext import ArrayField, JSONField
import os
import dotenv

dotenv.load_dotenv()

# Define the database connection
db = PostgresqlDatabase(
    "campsnatch",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=5432,
)

# Connect to the database once when the module is imported
db.connect()


# Define the Facility model
class Facility(Model):
    id = AutoField()
    source_id = TextField(null=True, unique=True)
    name = TextField(null=True)
    location = TextField(null=True)
    description = TextField(null=True)
    reservable = BooleanField(null=True)

    class Meta:
        database = db


# Define the Tracker model
class Tracker(Model):
    id = AutoField()
    user_id = TextField()
    device_token = TextField()
    facility_id = TextField()
    facility_name = TextField()
    start_date = DateField()
    end_date = DateField()

    class Meta:
        database = db


# Function to initialize the database
def initialize_db():
    # db.drop_tables([Tracker])
    # db.create_tables([Facility,Tracker])
    # db.create_tables([Device])
    pass


# Ensure the script can be run directly to initialize the database
if __name__ == "__main__":
    initialize_db()
