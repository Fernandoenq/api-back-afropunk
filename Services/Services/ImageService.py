from typing import List


class ImageService:
    @staticmethod
    def get_image_ids(cursor) -> List[str]:
        cursor.execute("SELECT ImageId FROM Image Where Active = 1 ORDER BY RegisterDate DESC")
        result = cursor.fetchall()

        return [str(row[0]) for row in result]
