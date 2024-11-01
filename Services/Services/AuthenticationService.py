import pandas as pd
import uuid
from Domain.Entities.Authentication import Authentication


class AuthenticationService:
    @staticmethod
    def get_authentication_by_id(cursor, authentication_id: int) -> pd.DataFrame:
        cursor.execute("Select AuthenticationId, IsSent From Authentication "
                       "Where AuthenticationId = %s", (authentication_id,))
        loaded_authentication = cursor.fetchall()

        authentication = Authentication()
        return pd.DataFrame(loaded_authentication, columns=[authentication.authentication_id, authentication.is_sent])

    @staticmethod
    def create_authentication(cursor):
        authentication_id = str(uuid.uuid4())

        cursor.execute("""INSERT INTO Authentication (AuthenticationId, IsSent) VALUES (%s, 0)""", (authentication_id,))

        if cursor.rowcount <= 0:
            return None

        return authentication_id

    @staticmethod
    def set_authentication_sent(cursor, authentication_id: int) -> bool:
        cursor.execute("""Update Authentication Set IsSent = 1 WHERE AuthenticationId = %s""", (authentication_id,))

        if cursor.rowcount <= 0:
            return False
