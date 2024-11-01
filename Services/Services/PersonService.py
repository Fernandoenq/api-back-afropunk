import pandas as pd
from Domain.Entities.Person import Person
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Services.Services.PortfolioService import PortfolioService


class PersonService:
    @staticmethod
    def get_person_by_cpf(cpf: str, cursor) -> pd.DataFrame:
        cursor.execute("Select PersonId, PersonName, Cpf, RegisterDate From Person Where Cpf = %s", (cpf,))
        loaded_person = cursor.fetchall()

        person = Person()
        return pd.DataFrame(loaded_person, columns=[person.person_id, person.person_name, person.cpf,
                                                    person.register_date])

    @staticmethod
    def create_person(person_request: PersonRequestModel, cursor) -> bool:
        person_df = PersonService().get_person_by_cpf(person_request.cpf, cursor)

        if person_df.empty:
            cursor.execute("""INSERT INTO Person (PersonName, Cpf, Phone, BirthDate, Mail, RegisterDate, 
                                HasAcceptedPromotion, HasAcceptedParticipation) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                           (person_request.person_name, person_request.cpf, person_request.phone, person_request.birth_date,
                            person_request.mail, person_request.register_date, person_request.has_accepted_promotion,
                            person_request.has_accepted_participation))

            if cursor.rowcount <= 0:
                return False

            person_id = cursor.lastrowid
        else:
            person = Person()
            person_id = int(person_df[person.person_id][0])

        return PortfolioService().create_portfolio(cursor, person_id, person_request.image_ids,
                                                   person_request.authentication_id)
