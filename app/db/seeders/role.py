import csv

from app.db.models import Role
from app.db.seeders.seeder import Seeder
from sqlalchemy.dialects.postgresql import insert

class RoleSeeder(Seeder):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self, session):
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            data = [
                { "name": stripped["name"].strip() }
                for row in reader
                for stripped in [{k.strip(): v for k, v in row.items()}]
            ]

        #session.bulk_insert_mappings(Gender, data)
        #session.commit()

        stmt = insert(Role).values(data)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        session.execute(stmt)
        session.commit()

        print(f"Seeded {len(data)} roles.")