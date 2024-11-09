from flask import jsonify
import traceback
from Services.Services.ConnectionService import ConnectionService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Services.Services.ImageService import ImageService


class ImageController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Image/Image', methods=['GET'])
        def get_image_ids():
            try:
                connection = ConnectionService.open_connection()
                cursor = connection.cursor()
                connection.start_transaction()

                try:
                    image_ids = ImageService().get_image_ids(cursor)

                    response_json = {
                        "image_ids": image_ids
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
