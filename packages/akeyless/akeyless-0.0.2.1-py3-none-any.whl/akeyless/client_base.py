import abc
import six
from akeyless_uam_api import GetItemReplyObj, GetUserItemsReplyObj

from akeyless.api import AkeylessApi
from akeyless.auth import ApiKeyAuthenticator, CredsRenewal
from akeyless.caching import KeyOperationsCredsCache
from akeyless.config import AkeylessClientConfig


@six.add_metaclass(abc.ABCMeta)
class AkeylessClientI(object):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        self.config = config
        self.api = AkeylessApi(self.config)
        self.auth = ApiKeyAuthenticator(self.api, config.policy_id, config.prv_key_seed)
        self.cr = CredsRenewal(self.auth)
        self.key_ops_cache = KeyOperationsCredsCache(self.api, self.cr)

    @abc.abstractmethod
    def encrypt_string(self, key_name, plaintext):
        # type: (str, str) -> str
        """Encrypts plaintext into ciphertext by using an AES key.

        :param str key_name: The name of the key to use in the encryption process (required)
        :param str plaintext: Data to be encrypted (required)
        :return: The encrypted data in base64 encoding.
        :rtype: str
        """

    @abc.abstractmethod
    def decrypt_string(self, key_name, ciphertext):
        # type: (str, str) -> str
        """Decrypts ciphertext into plaintext by using an AES key.

        :param str key_name: The name of the key to use in the decryption process (required)
        :param str ciphertext: Cipher to be decrypted in base64 encoding (required)
        :return: The decrypted data.
        :rtype: str
        """

    @abc.abstractmethod
    def encrypt_data(self, key_name, plaintext, associated_data=b""):
        # type: (str, bytes, bytes) -> bytes
        """Encrypts plaintext into ciphertext by using an AES key.

        :param str key_name: The name of the key to use in the encryption process (required)
        :param bytes plaintext: Data to be encrypted (required)
        :param bytes associated_data: Additional authenticated data (AAD) is any string that specifies the encryption
                                      context to be used for authenticated encryption. If used here, the same value must
                                      be supplied to the decrypt command or decryption will fail. (optional)
        :return: The encrypted data in bytes.
        :rtype: bytes
        """

    @abc.abstractmethod
    def decrypt_data(self, key_name, ciphertext, associated_data=b""):
        # type: (str, bytes, bytes) -> bytes
        """Decrypts ciphertext into plaintext by using an AES key.

        :param str key_name: The name of the key to use in the decryption process (required)
        :param bytes ciphertext: Cipher to be decrypted (required)
        :param bytes associated_data: The Additional authenticated data. If this was specified in the encrypt process,
                                      it must be specified in the decrypt process or the decryption operation will
                                      fail. (optional)
        :return: The decrypted data.
        :rtype: bytes
        """

    @abc.abstractmethod
    def describe_key(self, key_name):
        # type: (str) -> GetItemReplyObj
        """Return key details.

        :param str key_name: Key name (required)
        :return: The key details.
        :rtype: GetItemReplyObj
        """

    @abc.abstractmethod
    def describe_user_keys(self):
        # type: () -> GetUserItemsReplyObj
        """Return a list of all the keys associated with the user.

        :return: A list of all the keys associated with the user.
        :rtype: GetUserItemsReplyObj
        """

    def close(self):
        self.api.close()
