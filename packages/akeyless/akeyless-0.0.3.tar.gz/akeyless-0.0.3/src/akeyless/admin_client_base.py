import abc

import ecdsa
import six
from akeyless_uam_api import GetAccountDetailsReplyObj, GetUserReplyObj, GetRoleReplyObj

from akeyless.config import AkeylessClientConfig
from akeyless.crypto import CryptoAlgorithm
from akeyless.client_base import AkeylessClientI
from akeyless.utils import UserAccessApi
from akeyless.utils.structures import ApiKey


@six.add_metaclass(abc.ABCMeta)
class AkeylessAdminUserI(AkeylessClientI):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        super(AkeylessAdminUserI, self).__init__(config)

    @abc.abstractmethod
    def get_account_details(self):
        # type: () -> GetAccountDetailsReplyObj
        """Get account details.

        This endpoint is accessible only by the account admin user

        :return: The account details
        :rtype: GetAccountDetailsReplyObj
        """

    @abc.abstractmethod
    def create_aes_key(self, key_name, alg, user_metadata, split_level):
        # type: (str, CryptoAlgorithm, str, int) -> None
        """Creates a new AES key.

        This endpoint is accessible only by the account admin user

        :param str key_name: The key name to be created (required)
        :param CryptoAlgorithm alg: The algorithm for the key to be created. Types available are: [AES128GCM,
                                    AES256GCM, AES128SIV, AES256SIV] (required)
        :param str user_metadata: User metadata about the key. (required)
        :param int split_level: The splitting level represent the number of fragments that the key will be
                                split into. (required)
        """
    @abc.abstractmethod
    def update_key(self, new_key_name, key_name, user_metadata):
        # type: (str, str, str) -> None
        """Updating an existing key in the account

        This endpoint is accessible only by the account admin user

        :param str new_key_name: The new key name that will replace the existing one (required)
        :param str key_name: Key name. (required)
        :param str user_metadata: User metadata about the key.
        """

    @abc.abstractmethod
    def delete_key(self, key_name):
        # type: (str) -> None
        """Deleting an existing key from the account

        This endpoint is accessible only by the account admin user

        :param str key_name: Key name. (required)
        """

    @abc.abstractmethod
    def create_user(self, user_name, expires=0, cidr_whitelist=None):
        # type: (str, int, list) -> UserAccessApi
        """Add a new user to the account.

        This endpoint is accessible only by the account admin user

        :param str user_name: The user name to be created (required)
        :param int expires: User access expiration date in Unix timestamp. In case of 0 or null the user
                            access will not be limited in time.
        :param list cidr_whitelist: An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR
                                    list will be able to obtain temporary access credentials. The list length is
                                    limited to 10 CIDRs. In the case of an empty string there will be no restriction
                                    of IP addresses.
        :return: An object that contains the user name, policy id and access key
        :rtype: UserAccessApi
        """

    @abc.abstractmethod
    def get_user(self, user_name):
        # type: (str) -> GetUserReplyObj
        """Get user details.

        This endpoint is accessible only by the account admin user

        :param str user_name: User name. (required)
        :return: The user details
        :rtype: GetUserReplyObj
        """

    @abc.abstractmethod
    def update_user(self, new_user_name, user_name, expires=0, cidr_whitelist=None):
        # type: (str, str, int , list) -> None
        """Updating an existing user in the account

        This endpoint is accessible only by the account admin user

        :param str new_user_name: The new username that will replace the existing one (required)
        :param str user_name: User name. (required)
        :param int expires: User access expiration date in Unix timestamp. In case of 0 or null the user access will
                            not be limited in time.
        :param list cidr_whitelist: An CIDR Whitelisting. Only requests from the ip addresses that match the CIDR
                                    list will be able to obtain temporary access credentials. The list length is
                                    limited to 10 CIDRs. In the case of an empty string there will be no restriction
                                    of IP addresses
        """

    @abc.abstractmethod
    def reset_user_access_key(self, user_name):
        # type: (str) -> ApiKey
        """Replacing the user's access API key

        This endpoint is accessible only by the account admin user

        :param str user_name: User name. (required)
        :return: The new user access key
        :rtype: ApiKey
        """

    @abc.abstractmethod
    def delete_user(self, user_name):
        # type: (str) -> None
        """Deleting an existing user from the account.

        This endpoint is accessible only by the account admin user

        :param str user_name: User name. (required)
        """

    @abc.abstractmethod
    def create_role(self, role_name, role_action="", comment=""):
        # type: (str, str, str) -> None
        """Add a new role to the account.

        This endpoint is accessible only by the account admin user

        :param str role_name: The role name to be created (required)
        :param str role_action: The role action.
        :param str comment: Comments
        """

    @abc.abstractmethod
    def get_role(self, role_name):
        # type: (str) -> GetRoleReplyObj
        """Get role details.

        This endpoint is accessible only by the account admin user

        :param str role_name: Role name. (required)
        :return: The role details
        :rtype: GetRoleReplyObj
        """

    @abc.abstractmethod
    def update_role(self, new_role_name, role_name, role_action="", comment=""):
        # type: (str, str, str, str) -> None
        """Updating an existing role in the account

        This endpoint is accessible only by the account admin user

        :param str new_role_name: The new role name that will replace the existing one (required)
        :param str role_name: Role name. (required)
        :param str role_action: The role action.
        :param str comment: Comments
        """

    @abc.abstractmethod
    def delete_role(self, role_name):
        # type: (str) -> None
        """Deleting an existing role from the account.

        This endpoint is accessible only by the account admin role

        :param str role_name: Role name. (required)
        """

    @abc.abstractmethod
    def create_role_item_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        """Add an association between a role and an item.

        This endpoint is accessible only by the account admin user

        :param str role_name: The role name to be associated (required)
        :param str associated_name: The item or user name to be associated. (required)
        """

    @abc.abstractmethod
    def create_role_user_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        """Add an association between a role and a user.

        This endpoint is accessible only by the account admin user

        :param str role_name: The role name to be associated (required)
        :param str associated_name: The item or user name to be associated. (required)
        """

    @abc.abstractmethod
    def delete_role_item_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        """Deleting an association between a role and an item.

        This endpoint is accessible only by the account admin role

        :param str role_name: The role name to be associated (required)
        :param str associated_name: The item or user name to be associated. (required)
        """

    @abc.abstractmethod
    def delete_role_user_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        """Deleting an association between a role and an user.

        This endpoint is accessible only by the account admin role

        :param str role_name: The role name to be associated (required)
        :param str associated_name: The item or user name to be associated. (required)
        """