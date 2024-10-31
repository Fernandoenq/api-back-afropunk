from Services.Services.PersonService import PersonService
from flask import jsonify, request
import traceback
from Services.Services.ConnectionService import ConnectionService
from Services.Services.ValidationService import ValidationService
from Services.Services.SqsService import SqsService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Application.Models.Request.PersonRequestModel import PersonRequestModel


class PersonController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Person/Person', methods=['POST'])
        def register_person():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                person_request = request.get_json()
                person_request = PersonRequestModel(person_request)

                validations = ValidationService.validate_register_person(person_request, cursor)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                is_registered = PersonService.create_person(person_request, cursor)
                if is_registered is False:
                    return jsonify(ErrorResponseModel(
                        Errors=["Não foi possível realizar o cadastro. Tente novamente em alguns minutos"]).dict()), 422

                connection.commit()

                is_sent = SqsService().send_message_to_sqs(
                    person_request.phone, person_request.person_name, person_request.image_ids)
                if is_sent is False:
                    return jsonify(ErrorResponseModel(
                        Errors=["Não conseguimos enviar suas fotos. "
                                "Por favor, insira apenas o seu CPF e confirme novamente"]).dict()), 422

                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)
