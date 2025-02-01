from Services.Services.ConnectionService import ConnectionService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Services.Services.ImageService import ImageService
from Services.Services.ValidationService import ValidationService
from flask import jsonify, send_file, request
import traceback
from Application.Configuration import Configuration
import boto3
from io import BytesIO

s3_client = boto3.client(
    "s3",
    region_name=Configuration.region_name,
    aws_access_key_id=Configuration.aws_access_key_id,
    aws_secret_access_key=Configuration.aws_secret_access_key,
)


class ImageController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Image/Image/<image_id>', methods=['GET'])
        def get_image(image_id):
            try:
                file_object = BytesIO()
                s3_client.download_fileobj(Configuration.bucket_name, image_id, file_object)
                file_object.seek(0)

                return send_file(file_object, download_name=image_id, as_attachment=False)

            except s3_client.exceptions.ClientError as e:
                print(f"Arquivo não encontrado no S3: {image_id} | Ex: {e}")
                return jsonify(ErrorResponseModel(Errors=['Arquivo não encontrado']).dict()), 404
            except Exception as e:
                print(f"{str(e)} | {traceback.format_exc()}")
                return jsonify(ErrorResponseModel(Errors=['Erro interno do servidor']).dict()), 500

        @app.route('/Image/SaveImage', methods=['POST'])
        def save_image():
            try:
                connection = ConnectionService.open_connection()
                cursor = connection.cursor()
                connection.start_transaction()

                try:
                    file = request.files.get('file')
                    cpf = request.form.get('cpf')

                    validations = ValidationService.validate_activation(cpf, cursor)
                    if validations.is_valid is False:
                        return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                    image_name = ImageService().generate_external_file_id(file.filename)

                    is_saved = ImageService().save_image(file, image_name, cpf, cursor)
                    if is_saved is False:
                        return jsonify(ErrorResponseModel(Errors=["Não foi possível gerar imagem"]).dict()), 422

                    connection.commit()

                    return jsonify({
                        "image_name": image_name
                    }), 200

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
