from rest_framework import status
from rest_framework.exceptions import APIException


class APIAuthUserDoesNotExist(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Brukernavnet du har oppgitt tilhører ingen konto. Kontroller brukernavnet og prøv på nytt"
