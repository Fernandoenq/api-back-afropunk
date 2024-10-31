from typing import List


class WhatsAppModel:
    def __init__(self, phone, image_ids: List[str]):
        self.origin = 1
        self.phone = phone
        self.message = "Aqui estão suas fotos"
        self.image_ids = image_ids
