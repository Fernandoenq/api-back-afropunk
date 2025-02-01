from Services.Services.PersonService import PersonService
from flask import jsonify, request
import traceback
from Services.Services.ConnectionService import ConnectionService
from Services.Services.ValidationService import ValidationService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Application.Models.Request.PersonExternalCodeRequestModel import PersonExternalCodeModel


class PersonController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Person/Person', methods=['POST'])
        def register_person():
            try:
                connection = ConnectionService.open_connection()
                cursor = connection.cursor()
                connection.start_transaction()

                try:
                    person_request = request.get_json()
                    person_request = PersonRequestModel.to_map(person_request)

                    validations = ValidationService.validate_register_person(person_request, cursor)
                    if validations.is_valid is False:
                        return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                    is_registered = PersonService.create_person(person_request, cursor)
                    if is_registered is False:
                        return jsonify(ErrorResponseModel(
                            Errors=["Não foi possível realizar o cadastro. Tente novamente em alguns minutos"]).dict()), 422

                    connection.commit()

                    return jsonify(), 200

                except Exception as e:
                    if connection.is_connected():
                        connection.rollback()
                    error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                    return jsonify(error_response.dict()), 500
                finally:
                    if connection.is_connected():
                        ConnectionService.close_connection(cursor, connection)
            except Exception as e:
                print(f"{str(e)} | {traceback.format_exc()}")
                return jsonify(ErrorResponseModel(Errors=['Erro interno do servidor']).dict()), 500

        @app.route('/Person/SetExternalCode', methods=['PUT'])
        def set_external_code():
            try:
                connection = ConnectionService.open_connection()
                cursor = connection.cursor()
                connection.start_transaction()

                try:
                    person_request = request.get_json()
                    external_code_request = PersonExternalCodeModel.to_map(person_request)

                    validations = ValidationService.validate_external_code(external_code_request, cursor)
                    if validations.is_valid is False:
                        return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                    is_registered = PersonService.set_external_code(external_code_request, cursor)
                    if is_registered is False:
                        return jsonify(ErrorResponseModel(
                            Errors=[
                                "Não foi possível vincular o código ao participante"]).dict()), 422

                    connection.commit()

                    return jsonify(), 200

                except Exception as e:
                    if connection.is_connected():
                        connection.rollback()
                    error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                    return jsonify(error_response.dict()), 500
                finally:
                    if connection.is_connected():
                        ConnectionService.close_connection(cursor, connection)
            except Exception as e:
                print(f"{str(e)} | {traceback.format_exc()}")
                return jsonify(ErrorResponseModel(Errors=['Erro interno do servidor']).dict()), 500
