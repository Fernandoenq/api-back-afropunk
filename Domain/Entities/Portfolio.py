import pandas as pd
from Domain.Entities.Image import Image
from Domain.Entities.Person import Person


class Portfolio:
    def __init__(self):
        self.portfolio_id = 'PortfolioId'
        self.image_id = 'ImageId'
        self.person_id = 'PersonId'
        self.person = Person()
        self.image = Image()

        self.image_df = pd.DataFrame(columns=[self.portfolio_id, self.image_id, self.person_id])
