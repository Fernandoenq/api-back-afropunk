from typing import List
import pandas as pd
from Domain.Entities.Image import Image


class ImageService:
    @staticmethod
    def get_image_ids(cursor) -> List[str]:
        cursor.execute("SELECT ImageId FROM Image Where Active = 1 And IsDeleted = 0 ORDER BY RegisterDate DESC")
        result = cursor.fetchall()

        return [str(row[0]) for row in result]

    @staticmethod
    def has_image_id(cursor, image_ids: List[str]) -> bool:
        cursor.execute(
            f"""SELECT ImageId 
                    FROM Image 
                    WHERE IsDeleted = 0 
                    AND ImageId IN ({', '.join(['%s'] * len(image_ids))})""",
            tuple(image_ids)
        )
        image_loaded = cursor.fetchall()

        image = Image()
        image_df = pd.DataFrame(image_loaded, columns=[image.image_id])

        db_image_ids = set(image_df[image.image_id])
        return db_image_ids >= set(image_ids)
