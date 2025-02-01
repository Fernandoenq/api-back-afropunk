import pandas as pd
import datetime
from Domain.Entities.Calendar import Calendar


class CalendarService:
    @staticmethod
    def get_calendar(cursor) -> pd.DataFrame:
        cursor.execute("Select * From Calendar Where EventDay != 0")
        loaded_calendar = cursor.fetchall()

        calendar = Calendar()
        return pd.DataFrame(loaded_calendar, columns=[calendar.event_day_id, calendar.initial_date_time,
                                                      calendar.final_date_time])

    @staticmethod
    def get_calendar_to_transfer(cursor) -> pd.DataFrame:
        cursor.execute("Select EventDay, InitialDatetime From Calendar")
        loaded_calendar = cursor.fetchall()

        calendar = Calendar()
        calendar_df = pd.DataFrame(loaded_calendar, columns=[calendar.event_day_id, calendar.initial_date_time])
        calendar_df['InitialDatetime'] = pd.to_datetime(calendar_df['InitialDatetime'],
                                                        format='%a, %d %b %Y %H:%M:%S %Z')
        calendar_df['InitialDatetime'] = calendar_df['InitialDatetime'].dt.strftime('%Y-%m-%d')

        return calendar_df

    @staticmethod
    def get_completed_calendar(cursor) -> pd.DataFrame:
        cursor.execute("Select * From Calendar")
        loaded_calendar = cursor.fetchall()

        calendar = Calendar()
        return pd.DataFrame(loaded_calendar, columns=[calendar.event_day_id, calendar.initial_date_time,
                                                      calendar.final_date_time])

    @staticmethod
    def get_calendar_by_date(redistribution_date: datetime, cursor) -> pd.DataFrame:
        cursor.execute("SELECT * FROM Calendar WHERE %s BETWEEN InitialDatetime AND FinalDatetime",
                       (redistribution_date, ))
        loaded_calendar = cursor.fetchall()

        calendar = Calendar()
        return pd.DataFrame(loaded_calendar, columns=[calendar.event_day_id, calendar.initial_date_time,
                                                      calendar.final_date_time])

    @staticmethod
    def get_calendar_by_event_day(event_day: int, cursor) -> pd.DataFrame:
        cursor.execute("SELECT * FROM Calendar WHERE EventDay = %s",
                       (event_day,))
        loaded_calendar = cursor.fetchall()

        calendar = Calendar()
        return pd.DataFrame(loaded_calendar, columns=[calendar.event_day_id, calendar.initial_date_time,
                                                      calendar.final_date_time])

    @staticmethod
    def get_adjusted_event_date_today(date: datetime, cursor) -> pd.DataFrame:
        calendar = Calendar()
        calendar_df = CalendarService().get_calendar(cursor)

        calendar_df[calendar.initial_date_time] = pd.to_datetime(calendar_df[calendar.initial_date_time]).dt.normalize()
        calendar_df[calendar.final_date_time] = pd.to_datetime(
            calendar_df[calendar.final_date_time]).dt.normalize() + pd.Timedelta(hours=23, minutes=59, seconds=59)

        redistribution_date_df = pd.to_datetime(date).normalize()

        has_range = ((calendar_df[calendar.initial_date_time] <= redistribution_date_df)
                     & (calendar_df[calendar.final_date_time] >= redistribution_date_df))

        calendar_df = calendar_df[has_range]
        calendar_df = calendar_df.reset_index(drop=True)

        return calendar_df

    @staticmethod
    def update_event_day_to_redistributed(event_day: int, cursor):
        cursor.execute("UPDATE Calendar SET IsRedistributed = 1 WHERE EventDay = %s", (event_day, ))
