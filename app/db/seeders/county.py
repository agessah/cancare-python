import csv

from app.db.models import County
from app.db.seeders.seeder import Seeder
from sqlalchemy.dialects.postgresql import insert

class CountySeeder(Seeder):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self, session):
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            data = [
                {
                    "code": row.get("code", "").strip() if row.get("code") else None,
                    "name": row.get("name", "").strip() if row.get("name") else None,
                    "town": row.get("town", "").strip() if row.get("town") else None
                }
                for row in reader
                for stripped in [{k.strip(): v for k, v in row.items()}]
            ]

        #session.bulk_insert_mappings(County, data)
        #session.commit()

        stmt = insert(County).values(data)
        stmt = stmt.on_conflict_do_nothing(index_elements=["code"])
        session.execute(stmt)
        session.commit()

        print(f"Seeded {len(data)} counties.")