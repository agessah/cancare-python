from enum import Enum

class ConsultationStatus(str, Enum):
    SENT = "SENT"
    REVIEWED = "REVIEWED"

    def label(self):
        return {
            "SENT": "Sent",
            "REVIEWED": "Reviewed"
        }[self.value]