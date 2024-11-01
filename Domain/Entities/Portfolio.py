import pandas as pd
from Domain.Entities.Image import Image
from Domain.Entities.Person import Person
from Domain.Entities.Authentication import Authentication


class Portfolio:
    def __init__(self):
        self.portfolio_id = 'PortfolioId'
        self.image_id = 'ImageId'
        self.person_id = 'PersonId'
        self.authentication_id = 'AuthenticationId'
        self.person = Person()
        self.image = Image()
        self.authentication = Authentication()

        self.image_df = pd.DataFrame(columns=[self.portfolio_id, self.image_id,
                                              self.person_id, self.authentication_id])
