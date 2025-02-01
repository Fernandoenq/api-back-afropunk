from pydantic import BaseModel
from typing import Optional


class PersonExternalCodeModel(BaseModel):
    Cpf: str
    ExternalCode: str
    OrganizerId: int

    @classmethod
    def to_map(cls, json) -> "PersonExternalCodeModel":
        return cls(
            Cpf=json.get('Cpf'),
            ExternalCode=json.get('ExternalCode'),
            OrganizerId=json.get('OrganizerId')
        )
