import pandas as pd


class Person:
    def __init__(self):
        self.person_id = 'PersonId'
        self.person_name = 'PersonName'
        self.cpf = 'Cpf'
        self.phone = 'Phone'
        self.mail = 'Mail'
        self.register_date = 'RegisterDate'
        self.has_accepted_participation = 'HasAcceptedParticipation'
        self.external_code = 'ExternalCode'
        self.balance_current_value = 'BalanceCurrentValue'

        self.person_df = pd.DataFrame(columns=[self.person_id, self.person_name, self.cpf,
                                               self.phone, self.mail, self.register_date,
                                               self.has_accepted_participation, self.external_code,
                                               self.balance_current_value])
