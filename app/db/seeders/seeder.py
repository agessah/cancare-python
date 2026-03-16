from sqlalchemy.orm import Session

class Seeder:
    def run(self, session: Session):
        """Override this method to implement seeding logic."""
        raise NotImplementedError