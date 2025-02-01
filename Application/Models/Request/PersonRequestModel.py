from pydantic import BaseModel
from typing import Optional


class PersonRequestModel(BaseModel):
    PersonName: Optional[str]
    Cpf: str
    Phone: Optional[str]
    Mail: Optional[str]
    HasAcceptedTerm: bool

    @classmethod
    def to_map(cls, json) -> "PersonRequestModel":
        return cls(
            PersonName=json.get('PersonName'),
            Cpf=json.get('Cpf'),
            Phone=json.get('Phone'),
            Mail=json.get('Mail'),
            HasAcceptedTerm=json.get('HasAcceptedTerm')
        )
