from pydantic import BaseModel
from typing import Optional


class ActivationRequestModel(BaseModel):
    Cpf: str
    OrganizerId: int

    @classmethod
    def to_map(cls, json) -> "ActivationRequestModel":
        return cls(
            Cpf=json.get('Cpf'),
            OrganizerId=json.get('OrganizerId')
        )
