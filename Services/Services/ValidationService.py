from datetime import datetime
from Services.Models.Results.ValidationResult import ValidationResult
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Application.Models.Request.ActivationRequestModel import ActivationRequestModel
from Application.Models.Request.PersonExternalCodeRequestModel import PersonExternalCodeModel
from Application.Models.Request.OrganizerLoginRequestModel import OrganizerLoginRequestModel
from Services.Services.PersonService import PersonService
from Services.Services.OrganizerService import OrganizerService
from Domain.Entities.Person import Person
import pandas as pd


class ValidationService:
    @staticmethod
    def validate_register_person(person_request: PersonRequestModel, cursor) -> ValidationResult:
        result = ValidationResult()

        person_df = PersonService().get_person_by_cpf(person_request.Cpf, cursor)
        if person_df.empty is False:
            result.add_error("Você já se cadastrou")
            return result

        if person_request is None:
            result.add_error("Dados de requisição não enviados")
            return result

        if not person_request.HasAcceptedTerm:
            result.add_error("É necessário aceitar o termo de responsabilidade e segurança de acordo com LGPD")
            return result

        cpf_validation = ValidationService.validate_cpf(person_request.Cpf)
        if cpf_validation.is_valid is False:
            result.add_errors(cpf_validation.errors)
            return result

        return result

    @staticmethod
    def validate_external_code(external_code_request: PersonExternalCodeModel, cursor) -> ValidationResult:
        result = ValidationResult()

        cpf_validation = ValidationService.validate_cpf(external_code_request.Cpf)
        if cpf_validation.is_valid is False:
            result.add_errors(cpf_validation.errors)
            return result

        person_df = PersonService().get_person_by_cpf(external_code_request.Cpf, cursor)
        if person_df.empty:
            result.add_error("É necessário realizar o cadastro antes")
            return result

        person = Person()
        if pd.isna(person_df[person.external_code].iloc[0]) is False:
            result.add_error("Um código ja foi definido para o participante")
            return result

        return result

    @staticmethod
    def validate_activation(cpf: str, cursor) -> ValidationResult:
        result = ValidationResult()

        cpf_validation = ValidationService.validate_cpf(cpf)
        if cpf_validation.is_valid is False:
            result.add_errors(cpf_validation.errors)
            return result

        person_df = PersonService().get_person_by_cpf(cpf, cursor)
        if person_df.empty:
            result.add_error("É necessário realizar o cadastro antes")
            return result

        return result

    @staticmethod
    def validate_cpf(request_cpf: str) -> ValidationResult:
        result = ValidationResult()

        cpf = request_cpf

        if len(cpf) != 11:
            result.add_error(f"CPF inválido! Este CPF possui {len(cpf)} dígitos")
            return result

        if cpf == cpf[0] * 11 or cpf == '0' * 11:
            result.add_error("CPF inválido!")
            return result

        sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_digits * 10 % 11) % 10

        sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_digits * 10 % 11) % 10

        if cpf[-2:] != f"{first_digit}{second_digit}":
            result.add_error("CPF inválido!")

        return result

    @staticmethod
    def underage_verifier(award_date: str) -> ValidationResult:
        today = datetime.today().date()
        award_date_converted = datetime.strptime(award_date.split()[0], "%Y-%m-%d").date()
        age = today.year - award_date_converted.year

        if (today.month, today.day) < (award_date_converted.month, award_date_converted.day):
            age -= 1

        result = ValidationResult()
        if age < 18:
            result.add_error("De acordo com o regulamento da promoção, não é permitida a participação de menores.")
            return result

        return result

    @staticmethod
    def validate_login(login_request: OrganizerLoginRequestModel, cursor) -> ValidationResult:
        result = ValidationResult()

        organizer_df = OrganizerService().get_organizer_by_login(login_request.login, cursor)
        if organizer_df.empty:
            result.add_error("Dados incorretos")
            return result

        return result
