import json

from utils.crypto import rsa


class UOMeTools:
    @staticmethod
    def sign(private_key, group_uuid, issuer, borrower, value, description, uome_uuid):

        array = [group_uuid, issuer, borrower, str(value), description, uome_uuid]
        return rsa.sign(private_key, *array)

    @staticmethod
    def verify(public_key, signature, group_uuid, issuer, borrower, value, description,
               uome_uuid):

        array = [group_uuid, issuer, borrower, str(value), description, uome_uuid]
        return rsa.verify(public_key, signature, *array)
