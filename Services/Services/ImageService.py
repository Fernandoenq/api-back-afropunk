from botocore.exceptions import BotoCoreError, NoCredentialsError, PartialCredentialsError
import uuid
import os
import boto3
from werkzeug.datastructures import FileStorage
from Application.Configuration import Configuration
from typing import List
from Services.Services.PersonService import PersonService
from Application.Models.Request.ActivationRequestModel import ActivationRequestModel
from Domain.Entities.Person import Person
from datetime import datetime


class ImageService:
    @staticmethod
    def save_image(file: FileStorage, file_name: str, cpf: str, cursor) -> bool:
        person_df = PersonService.get_person_by_cpf(cpf, cursor)
        person = Person()
        person_id = int(person_df[person.person_id][0])

        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=Configuration.aws_access_key_id,
                aws_secret_access_key=Configuration.aws_secret_access_key,
                region_name=Configuration.region_name
            )

            s3_client.upload_fileobj(file, Configuration.bucket_name, file_name)

            cursor.execute("""INSERT INTO Image (ImageName, PersonId, RegisterDate) 
                                VALUES (%s, %s, %s)""", (file_name, person_id, datetime.now()))

            if cursor.rowcount <= 0:
                return False

            return True
        except (BotoCoreError, NoCredentialsError, PartialCredentialsError) as e:
            print(f"Erro ao fazer upload para o S3: {e}")
            return False

    @staticmethod
    def generate_external_file_id(file_name) -> str:
        _, file_extension = os.path.splitext(file_name)
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"
