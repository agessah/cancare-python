from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.seeders.county import CountySeeder
from app.db.seeders.gender import GenderSeeder
from app.db.seeders.subcounty import SubCountySeeder
from app.db.seeders.user import UserSeeder

engine = create_engine("postgresql+psycopg2://postgres:9128@localhost:5432/cancer-care", echo=True)
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