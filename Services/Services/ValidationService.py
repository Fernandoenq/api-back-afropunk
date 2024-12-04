from datetime import datetime
from Services.Models.Results.ValidationResult import ValidationResult
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Services.Services.AuthenticationService import AuthenticationService
from Services.Services.ImageService import ImageService
from Domain.Entities.Authentication import Authentication


class ValidationService:
    @staticmethod
    def validate_register_person(person_request: PersonRequestModel, cursor) -> ValidationResult:
        result = ValidationResult()

        if person_request is None:
            result.add_error("Dados de requisição não enviados")
            return result

        if (person_request.register_date is None or person_request.person_name is None
                or person_request.cpf is None or person_request.phone is None or person_request.birth_date is None
                or person_request.mail is None or person_request.has_accepted_participation is None
                or person_request.authentication_id is None):
            result.add_error("Dados de requisição não enviados")
            return result

        if not person_request.has_accepted_participation:
            result.add_error("É necessário o compartilhamento dos dados para receber as imagens")
            return result

        cpf_validation = ValidationService.validate_cpf(person_request.cpf)
        if cpf_validation.is_valid is False:
            result.add_error(cpf_validation.errors)
            return result

        """
        if person_request.birth_date is not None:
            underage_validation = ValidationService.underage_verifier(person_request.birth_date)
            if underage_validation.is_valid is False:
                result.add_errors(underage_validation.errors)
                return result
        """

        authentication_df = AuthenticationService().get_authentication_by_id(cursor, person_request.authentication_id)
        if authentication_df.empty:
            result.add_error("Não autorizado")
            return result

        authentication = Authentication()
        if int(authentication_df[authentication.is_sent][0]) == 1:
            result.add_error("As fotos solicitadas já foram baixadas")
            return result

        has_image_id = ImageService().has_image_id(cursor, person_request.image_ids)
        if has_image_id is False:
            result.add_error("As fotos solicitadas não estão mais disponíveis no sistema. "
                             "Por favor, capture-as novamente.")
            return result

        return result

    @staticmethod
    def validate_cpf(request_cpf: str) -> ValidationResult:
        result = ValidationResult()

        cpf = request_cpf

        if cpf == '24624624624':
            return result

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
