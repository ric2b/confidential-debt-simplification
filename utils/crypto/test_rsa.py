from pytest import raises

from utils.crypto import rsa


class TestRSA:

    def test_SigningSomeTextWithKey1AndVerifyingWithPubkey1_DoesNotRaiseInvalidSignature(self):
        plain_text = "some text"
        key, pubkey = rsa.generate_keys()

        valid_signature = rsa.sign(key, plain_text)
        rsa.verify(pubkey, valid_signature, plain_text)

    def test_SigningSomeTextWithKey1AndVerifyingWithPubkey1_RaisesInvalidSignature(self):
        plain_text = "some text"
        key_1, pubkey_1 = rsa.generate_keys()
        key_2, pubkey_2 = rsa.generate_keys()

        with raises(rsa.InvalidSignature):
            valid_signature = rsa.sign(key_1, plain_text)
            rsa.verify(pubkey_2, valid_signature, plain_text)
