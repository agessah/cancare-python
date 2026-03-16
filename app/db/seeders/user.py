from app.core.security import hash_password
from app.db.models import User
from app.db.seeders.seeder import Seeder

class UserSeeder(Seeder):
    def run(self, session):
        existing = session.query(User).filter_by(email="admin@cancer-care.com").first()
        if existing:
            print("User already exists.")
            return

        user = User(
            name="System Admin",
            phone="0721135155",
            email="admin@cancer-care.com",
            password=hash_password("Admin@123"),
            active=True
        )

        session.add(user)
        session.commit()

        print("Seeded default admin user.")