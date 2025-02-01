from Application.Constants import Constants
from Domain.Enums.Operation import Operation
from Domain.Enums.Origin import Origin
from datetime import datetime


class BalanceService:
    @staticmethod
    def set_first_balance(person_id, organizer_id, event_day_id, cursor) -> bool:
        cursor.execute("""INSERT INTO Balance (Impact, BalanceCurrentValue, Operation, ImpactDate, ImpactOrigin, 
                        PersonId, OrganizerId, EventDayId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (Constants.first_balance, Constants.first_balance, Operation.addition.value, datetime.now(),
                        Origin.register.value, person_id, organizer_id, event_day_id))

        return cursor.rowcount > 0
