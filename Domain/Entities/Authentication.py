import pandas as pd


class Authentication:
    def __init__(self):
        self.authentication_id = 'AuthenticationId'
        self.is_sent = 'IsSent'

        self.person_df = pd.DataFrame(columns=[self.authentication_id, self.is_sent])
