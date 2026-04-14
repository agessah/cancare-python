from datetime import date

class UtilsService:
    @staticmethod
    def get_age(dob: date) -> int:
        today = date.today()
        return today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )