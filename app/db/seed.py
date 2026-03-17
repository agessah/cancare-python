from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.seeders.county import CountySeeder
from app.db.seeders.gender import GenderSeeder
from app.db.seeders.subcounty import SubCountySeeder
from app.db.seeders.user import UserSeeder

import os
db_url = os.getenv("DATABASE_URL", "").replace("asyncpg", "psycopg2")
engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

session = SessionLocal()
seeders = [
    CountySeeder("app/db/data/counties.csv"),
    SubCountySeeder("app/db/data/subcounties.csv"),
    GenderSeeder("app/db/data/genders.csv"),
    UserSeeder()
]

for seeder in seeders:
    seeder.run(session)

session.close()
print("All seeders executed!")