from pytest import fixture
from pytest import raises

from utils.crypto import rsa


class TestRSA:

    @fixture
    def tmpfile(self, tmpdir):
        return str(tmpdir.join("keyfile.pem"))

    def test_VerifyingACompletelyBrokenSignature_RaisesInvalidSignature(self):
        key, pubkey = rsa.generate_keys()

        with raises(rsa.InvalidSignature):
            rsa.verify(pubkey, "completelyBogûsÇigna_!ture", "not a chance!")

    def test_SigningSomeNonStringValues(self):
        values = ["hey", 10, 56.4, 'ho']
        key, pubkey = rsa.generate_keys()
        
        rsa.sign(key, *values)

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

    def test_DumpingAPrivateKeyAndLoadingTheRespectiveReturnsTheSameKey(self, tmpfile):
        key, pubkey = rsa.generate_keys()

        rsa.dump_key(key, tmpfile)
        loaded_key, loaded_pubkey = rsa.load_keys(tmpfile)

        assert key == loaded_key
        assert pubkey == loaded_pubkey

    def test_DumpingAPrivateKeyWithPasswordAndLoadingTheRespectiveReturnsTheSameKey(self, tmpfile):
        key, pubkey = rsa.generate_keys()

        rsa.dump_key(key, tmpfile, password="1234")
        loaded_key, loaded_pubkey = rsa.load_keys(tmpfile, password="1234")

        assert key == loaded_key
        assert pubkey == loaded_pubkey

    def test_DumpingAPublicKeyAndLoadingTheRespectiveReturnsTheSameKey(self,  tmpfile):
        key, pubkey = rsa.generate_keys()

        rsa.dump_pubkey(pubkey, tmpfile)
        loaded_pubkey = rsa.load_pubkey(tmpfile)

        assert pubkey == loaded_pubkey
