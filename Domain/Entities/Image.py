import pandas as pd


class Image:
    def __init__(self):
        self.image_id = 'ImageId'
        self.image_name = 'ImageName'
        self.register_date = 'RegisterDate'
        self.active = 'Active'
        self.is_deleted = 'IsDeleted'

        self.image_df = pd.DataFrame(columns=[self.image_id, self.image_name, self.register_date, self.active,
                                              self.is_deleted])
