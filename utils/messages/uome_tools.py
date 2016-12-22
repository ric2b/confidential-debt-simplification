import json

from utils.crypto import rsa


class UOMeTools:
    @staticmethod
    def issuer_sign(signing_key, group_uuid, issuer, borrower, value, description):

        array = [group_uuid, issuer, borrower, str(value), description]
        return rsa.sign(signing_key, *array)

    @staticmethod
    def issuer_verify(public_key, signature, group_uuid, issuer, borrower, value,
                      description):

        array = [group_uuid, issuer, borrower, str(value), description]
        return rsa.verify(public_key, signature, *array)

    @staticmethod
    def borrower_sign(signing_key, group_uuid, issuer, borrower, value, description,
                      uome_uuid):

        array = [group_uuid, issuer, borrower, value, description, uome_uuid]
        return rsa.sign(signing_key, *array)

    @staticmethod
    def borrower_verify(public_key, signature, group_uuid, issuer, borrower, value,
                        description, uome_uuid):

        array = [group_uuid, issuer, borrower, str(value), description, uome_uuid]
        print(json.dumps(array))
        return rsa.verify(public_key, signature, *array)
