import pandas as pd
from Domain.Entities.Person import Person
from Domain.Entities.Calendar import Calendar
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Application.Models.Request.PersonExternalCodeRequestModel import PersonExternalCodeModel
from datetime import datetime
from Application.Constants import Constants
from Services.Services.BalanceService import BalanceService
from Services.Services.CalendarService import CalendarService


class PersonService:
    @staticmethod
    def get_person_by_cpf(cpf: str, cursor) -> pd.DataFrame:
        cursor.execute("Select PersonId, PersonName, Cpf, RegisterDate, ExternalCode From Person Where Cpf = %s", (cpf,))
        loaded_person = cursor.fetchall()

        person = Person()
        return pd.DataFrame(loaded_person, columns=[person.person_id, person.person_name, person.cpf,
                                                    person.register_date, person.external_code])

    @staticmethod
    def create_person(person_request: PersonRequestModel, cursor) -> bool:
        cursor.execute("""INSERT INTO Person (PersonName, Cpf, Phone, Mail, HasAcceptedParticipation, RegisterDate) 
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                       (person_request.PersonName, person_request.Cpf, person_request.Phone, person_request.Mail,
                        person_request.HasAcceptedTerm, datetime.now()))

        if cursor.rowcount <= 0:
            return False

        return True

    @staticmethod
    def set_external_code(external_code_request: PersonExternalCodeModel, cursor) -> bool:
        cursor.execute("""Update Person Set ExternalCode = %s, BalanceCurrentValue = %s Where Cpf = %s""",
                       (external_code_request.ExternalCode, Constants.first_balance, external_code_request.Cpf))

        if cursor.rowcount <= 0:
            return False

        person = Person()
        person_df = PersonService.get_person_by_cpf(external_code_request.Cpf, cursor)
        person_id = int(person_df[person.person_id][0])

        calendar = Calendar()
        calendar_df = CalendarService().get_calendar_by_date(datetime.now(), cursor)
        event_day_id = int(calendar_df[calendar.event_day_id][0])

        return BalanceService().set_first_balance(person_id, external_code_request.OrganizerId, event_day_id, cursor)
