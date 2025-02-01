import pandas as pd
from Domain.Entities.Person import Person


class Image:
    def __init__(self):
        self.image_id = 'ImageId'
        self.image_name = 'ImageName'
        self.register_date = 'RegisterDate'
        self.is_downloaded = 'IsDownloaded'
        self.person_id = 'PersonId'
        self.person = Person()

        self.image_df = pd.DataFrame(columns=[self.image_id, self.image_name, self.register_date, self.is_downloaded,
                                              self.person_id])
