from flask import jsonify
import traceback
from Services.Services.ConnectionService import ConnectionService
from Services.Services.AuthenticationService import AuthenticationService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel


class AuthenticationController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Authentication/GenerateAuthenticationId', methods=['POST'])
        def generate_authentication_id():
            try:
                connection = ConnectionService.open_connection()
                cursor = connection.cursor()
                connection.start_transaction()

                try:
                    authentication_id = AuthenticationService().create_authentication(cursor)

                    if authentication_id is None:
                        return jsonify(ErrorResponseModel(
                            Errors=["Não foi possível gerar o AuthenticationId"]).dict()), 422

                    connection.commit()

                    response_json = {
                        "AuthenticationId": authentication_id
                    }

                    return jsonify(response_json), 200

                except Exception as e:
                    if connection.is_connected():
                        connection.rollback()
                    error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                    return jsonify(error_response.dict()), 500
                finally:
                    if connection.is_connected():
                        ConnectionService.close_connection(cursor, connection)
            except Exception as e:
                return jsonify('Erro servidor'), 500
