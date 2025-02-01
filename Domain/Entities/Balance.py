import pandas as pd
from Domain.Entities.Organizer import Organizer
from Domain.Entities.Person import Person
from Domain.Entities.Calendar import Calendar


class Balance:
    def __init__(self):
        self.balance_id = 'BalanceId'
        self.impact = 'Impact'
        self.balance_current_value = 'BalanceCurrentValue'
        self.operation = 'Operation'
        self.impact_date = 'ImpactDate'
        self.impact_origin = 'ImpactOrigin'
        self.person_id = 'PersonId'
        self.organizer_id = 'OrganizerId'
        self.event_day_id = 'EventDayId'
        self.person = Person()
        self.organizer = Organizer()
        self.calendar = Calendar()

        self.balance_df = pd.DataFrame(columns=[self.balance_id, self.impact, self.balance_current_value,
                                                self.operation, self.impact_date,
                                                self.impact_origin, self.person_id,
                                                self.organizer_id, self.event_day_id])

