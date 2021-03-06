from kavenegar import *
from VLE.config import config


def send(receptor, message):
    try:
        api = KavenegarAPI(config.KAVENEGAR_API_KEY)
        params = {
            'sender': '',
            'receptor': receptor,
            'message': message,
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
