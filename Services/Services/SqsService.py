import boto3
import json
from Application.Configuration import Configuration
from Services.Models.WhatsAppModel import WhatsAppModel


class SqsService:
    @staticmethod
    def send_message_to_sqs(whatsapp: WhatsAppModel, person_name: str) -> bool:
        sqs_client = boto3.client(
            "sqs",
            aws_access_key_id=Configuration.aws_access_key_id,
            aws_secret_access_key=Configuration.aws_secret_access_key,
            region_name=Configuration.region_name
        )

        response = sqs_client.send_message(
            QueueUrl=Configuration.sqs_queue_url,
            MessageBody=json.dumps(whatsapp)
        )

        if response.get('MessageId'):
            print(f"Mensagem enviada com sucesso para {person_name} / {whatsapp.phone}."
                  f"ID da mensagem: {response['MessageId']}")

            return True
        else:
            print(f"Falha ao enviar mensagem para {person_name} / {whatsapp.phone}.")
            return False
