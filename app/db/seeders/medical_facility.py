import pandas as pd

from app.db.models import MedicalFacility
from app.db.seeders.seeder import Seeder
from sqlalchemy.dialects.postgresql import insert

class MedicalFacilitySeeder(Seeder):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self, session):
        df = pd.read_excel(self.file_path)

        column_mapping = {
            "Hospital Name": "name",
            "County": "county_id",
            "Sub-County": "sub_county_id"
        }

        df = df.rename(columns=column_mapping)

        expected_columns = ["name", "county_id", "sub_county_id"]
        df = df[[col for col in expected_columns if col in df.columns]]

        df.columns = [col.strip() for col in df.columns]

        df = df.where(pd.notnull(df), None)

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(
                    lambda x: x.strip() if isinstance(x, str) else x
                )

        data = df.to_dict('records')

        stmt = insert(MedicalFacility).values(data)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        session.execute(stmt)
        session.commit()

        print(f"Seeded {len(data)} medical facilities.")