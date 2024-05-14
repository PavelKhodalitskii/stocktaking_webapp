import qrcode
from config.settings import MEDIA_ROOT, ALLOWED_HOSTS
from django.urls import reverse

# Генерирует QR-code для InvetoryItem
def generate_qr_code(obj):
    filename = obj.name + str(obj.id)
    url = "https://" + 'localhost:8000' + reverse("approve_item", kwargs={'item_id': obj.id})
    print(url)
    file_path = MEDIA_ROOT + "/qr_codes/" + filename + '.png'
    image_path = "/media/qr_codes/" + filename + '.png'
    img = qrcode.make(url)
    img.save(file_path)
    return image_path