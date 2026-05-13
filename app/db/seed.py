from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.seeders.county import CountySeeder
from app.db.seeders.gender import GenderSeeder
from app.db.seeders.level import LevelSeeder
from app.db.seeders.document_category import DocumentCategorySeeder
from app.db.seeders.media_type import MediaTypeSeeder
from app.db.seeders.follow_up_status import FollowUpStatusSeeder
from app.db.seeders.medical_facility import MedicalFacilitySeeder
from app.db.seeders.subcounty import SubCountySeeder
from app.db.seeders.role import RoleSeeder
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
    LevelSeeder("app/db/data/levels.csv"),
    FollowUpStatusSeeder("app/db/data/follow_up_statuses.csv"),
    DocumentCategorySeeder("app/db/data/document_categories.csv"),
    MediaTypeSeeder("app/db/data/media_types.csv"),
    MedicalFacilitySeeder("app/db/data/sha_public_hospitals.xlsx"),
    RoleSeeder("app/db/data/roles.csv"),
    UserSeeder()
]

for seeder in seeders:
    seeder.run(session)

session.close()
print("All seeders executed!")