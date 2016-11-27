from utils.crypto import rsa


class TestCrypto:
    """
    Here we include tests for the crypto package. We didn't follow the
    test case naming convention since it didn't make sense to tests
    the private key and public keys classes and the rsa module separately.
    """

    def test_Encrypt_OriginalText_EncryptedTextIsDifferentFromOriginal(self):
        plain_text = b"original text"
        privkey, pubkey = rsa.generate_keys()

        assert pubkey.encrypt(plain_text) != plain_text

    def test_Decrypt_EncryptedText_OriginalText(self):
        plain_text = b"original text"
        privkey, pubkey = rsa.generate_keys()
        encrypted_text = pubkey.encrypt(plain_text)

        assert privkey.decrypt(encrypted_text) == plain_text

    def test_Verify_SomeTextSignedWithCorrectPrivateKey_Succeeds(self):
        plain_text = b"some text"
        privkey, pubkey = rsa.generate_keys()
        valid_signature = privkey.sign(plain_text)

        assert pubkey.verify(valid_signature, plain_text)

    def test_Verify_SomeTextSignedWithIncorrectPrivateKey_Fails(self):
        plain_text = b"some text"
        privkey_1, pubkey_1 = rsa.generate_keys()
        privkey_2, pubkey_2 = rsa.generate_keys()

        invalid_signature = privkey_1.sign(plain_text)

        assert not pubkey_2.verify(plain_text, invalid_signature)

