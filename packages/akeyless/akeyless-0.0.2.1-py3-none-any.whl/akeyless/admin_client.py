import base64

import ecdsa
from hashlib import sha256

from akeyless_auth_api import SetUAMPolicyCredsParams
from akeyless_uam_api import GetAccountDetailsReplyObj, PolicyRules, GetRoleReplyObj

from akeyless.admin_client_base import AkeylessAdminUserI
from akeyless.config import AkeylessClientConfig
from akeyless.crypto import CryptoAlgorithm
from akeyless.client import AkeylessClient
from akeyless.utils import UserAccessApi
from akeyless.utils.structures import ApiKey


class AkeylessAdminClient(AkeylessAdminUserI, AkeylessClient):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        super(AkeylessAdminClient, self).__init__(config)

    def get_account_details(self):
        # type: () -> GetAccountDetailsReplyObj
        return self.api.get_account_details(self.cr.get_uam_creds())

    def create_aes_key(self, key_name, alg, user_metadata, split_level):
        # type: (str, CryptoAlgorithm, str, int) -> None
        return self.api.create_aes_key_item(self.cr.get_uam_creds(), key_name, alg, user_metadata, split_level)

    def update_key(self, new_key_name, key_name, user_metadata):
        # type: (str, str, str) -> None
        return self.api.update_item(self.cr.get_uam_creds(), new_key_name, key_name, user_metadata=user_metadata)

    def delete_key(self, key_name):
        # type: (str) -> None
        return self.api.delete_item(self.cr.get_uam_creds(), key_name)

    def create_user(self, user_name, expires=0, cidr_whitelist=None):
        # type: (str, int, list) -> UserAccessApi
        api_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=sha256)
        pub_key_der = api_key.get_verifying_key().to_der()
        pub_key_encoded = base64.b64encode(pub_key_der).decode()
        cidr_str = ""
        if cidr_whitelist is not None:
            cidr_str = ','.join(cidr_whitelist)

        rules = PolicyRules(alg="ECDSA_P256_SHA256", cidr_whitelist=cidr_str, key=pub_key_encoded)
        policy_params = SetUAMPolicyCredsParams(expires, "api_key", rules, None)

        set_policy_creds = self.api.set_uam_policy_creds(self.cr.get_auth_creds(), policy_params)
        res = self.api.create_user(self.cr.get_uam_creds(), set_policy_creds.credential, user_name)

        return UserAccessApi(user_name, res.user_policy_id, api_key)

    def get_user(self, user_name):
        # type: (str) -> ecdsa.SigningKey
        return self.api.get_user(self.cr.get_uam_creds(), user_name)

    def update_user(self, new_user_name, user_name, expires=None, cidr_whitelist=None):
        # type: (str, str, int, list) -> None

        update_modes = ["update_name"]
        rules = None
        if expires is not None:
            update_modes.append("update_exp")

        if cidr_whitelist is not None:
            rules = PolicyRules(cidr_whitelist=','.join(cidr_whitelist))
            update_modes.append("update_cidr")

        policy_params = SetUAMPolicyCredsParams(expires, "api_key", rules, update_modes)
        set_policy_creds = self.api.set_uam_policy_creds(self.cr.get_auth_creds(), policy_params)
        return self.api.update_user(self.cr.get_uam_creds(), set_policy_creds.credential, new_user_name, user_name)

    def reset_user_access_key(self, user_name):
        # type: (str) -> ApiKey
        api_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p, hashfunc=sha256)
        pub_key_der = api_key.get_verifying_key().to_der()
        pub_key_encoded = base64.b64encode(pub_key_der).decode()

        rules = PolicyRules(alg="ECDSA_P256_SHA256", key=pub_key_encoded)
        policy_params = SetUAMPolicyCredsParams(None, "api_key", rules, ["update_key"])

        set_policy_creds = self.api.set_uam_policy_creds(self.cr.get_auth_creds(), policy_params)
        self.api.update_user(self.cr.get_uam_creds(), set_policy_creds.credential, user_name, user_name)

        return ApiKey(api_key)

    def delete_user(self, user_name):
        # type: (str) -> None
        return self.api.delete_user(self.cr.get_uam_creds(), user_name)

    def create_role(self, role_name, role_action="", comment=""):
        # type: (str, str, str) -> None
        return self.api.create_role(self.cr.get_uam_creds(), role_name, role_action=role_action, comment=comment)

    def get_role(self, role_name):
        # type: (str) -> GetRoleReplyObj
        return self.api.get_role(self.cr.get_uam_creds(), role_name)

    def update_role(self, new_role_name, role_name, role_action="", comment=""):
        # type: (str, str, str, str) -> None
        return self.api.update_role(self.cr.get_uam_creds(), new_role_name, role_name,
                                    role_action=role_action, comment=comment)

    def delete_role(self, role_name):
        # type: (str) -> None
        return self.api.delete_role(self.cr.get_uam_creds(), role_name)

    def create_role_item_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        return self.api.create_role_item_assoc(self.cr.get_uam_creds(), role_name, associated_name)

    def create_role_user_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        return self.api.create_role_user_assoc(self.cr.get_uam_creds(), role_name, associated_name)

    def delete_role_item_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        return self.api.delete_role_item_assoc(self.cr.get_uam_creds(), role_name, associated_name)

    def delete_role_user_assoc(self, role_name, associated_name):
        # type: (str, str) -> None
        return self.api.delete_role_user_assoc(self.cr.get_uam_creds(), role_name, associated_name)
