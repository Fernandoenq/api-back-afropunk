import pandas as pd


class Calendar:
    def __init__(self):
        self.event_day_id = 'EventDayId'
        self.initial_date_time = 'InitialDatetime'
        self.final_date_time = 'FinalDatetime'

        self.calendar_df = pd.DataFrame(columns=[self.event_day_id, self.initial_date_time, self.final_date_time])
