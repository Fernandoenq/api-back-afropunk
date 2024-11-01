from typing import List


class PortfolioService:
    @staticmethod
    def create_portfolio(cursor, person_id: int, image_ids: List[str], authentication_id: str) -> bool:
        for i, image_id in enumerate(image_ids):
            cursor.execute("""INSERT INTO Portfolio (PersonId, ImageId, AuthenticationId) 
                            VALUES (%s, %s, %s)""",
                           (person_id, image_id, authentication_id,))

            if cursor.rowcount <= 0:
                return False

        return True
