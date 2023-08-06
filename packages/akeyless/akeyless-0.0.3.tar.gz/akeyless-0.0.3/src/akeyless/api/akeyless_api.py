import base64

from akeyless_auth_api.api_client import ApiClient as AuthApiClient
from akeyless_auth_api.configuration import Configuration as AuthApiConfiguration
from akeyless_auth_api import DefaultApi as AuthApi, SystemUserCredentialsReplyObj, SetUAMPolicyCredsParams, \
    CredentialsReplyObj

from akeyless_uam_api.api_client import ApiClient as UamApiClient
from akeyless_uam_api.configuration import Configuration as UamApiConfiguration
from akeyless_uam_api import DefaultApi as UamApi, DerivationCredsReplyObj, RSADecryptCredsReplyObj, \
    GetAccountDetailsReplyObj, GetItemReplyObj, GetUserItemsReplyObj, CreateUserReplyObj, GetUserReplyObj, \
    GetRoleReplyObj

from akeyless_kfm_api.api_client import ApiClient as KfmApiClient
from akeyless_kfm_api.configuration import Configuration as KfmApiConfiguration
from akeyless_kfm_api import DefaultApi as KfmApi

from akeyless.api.base import AkeylessApiI
from akeyless.config import AkeylessClientConfig
from akeyless.crypto import CryptoAlgorithm
from akeyless.crypto.utils import xor_fragments


class AkeylessApi(AkeylessApiI):

    def __init__(self, config):
        # type: (AkeylessClientConfig) -> None
        super(AkeylessApi, self).__init__(config)

        self.config = config
        self._init_api_clients()

    def get_account_details(self, akeyless_uam_user_creds, **kwargs):
        # type: (str, dict) -> GetAccountDetailsReplyObj
        return self.uam_api.get_account_details(akeyless_uam_user_creds, **kwargs)

    def authenticate_uam_api_key_policy(self, policy_id, timestamp, nonce, signature, **kwargs):
        # type: (str, int, str, str, dict) -> SystemUserCredentialsReplyObj
        return self.auth_api.authenticate_uam_api_key_policy(policy_id, timestamp, nonce, signature, **kwargs)

    def set_uam_policy_creds(self, akeyless_auth_creds, body, **kwargs):
        # type: (str, SetUAMPolicyCredsParams, dict) -> CredentialsReplyObj
        return self.auth_api.set_uam_policy_creds(akeyless_auth_creds, body, **kwargs)

    def get_item_derivation_creds(self, akeyless_uam_user_creds, item_name, **kwargs):
        # type: (str, str, dict) -> DerivationCredsReplyObj
        return self.uam_api.get_item_derivation_creds(akeyless_uam_user_creds, item_name, **kwargs)

    def get_rsa_key_decrypt_creds(self, akeyless_uam_user_creds, item_name, **kwargs):
        # type: (str, str, dict) -> RSADecryptCredsReplyObj
        return self.uam_api.get_rsa_key_decrypt_creds(akeyless_uam_user_creds, item_name, **kwargs)

    def derive_key(self, derivation_creds, kfm_user_creds, derivations_data, double_derivation=False):
        # type: (DerivationCredsReplyObj, str, list, bool) -> (bytes, list)
        return self._derive_key(derivation_creds, kfm_user_creds, derivations_data, double_derivation)

    def create_aes_key_item(self, akeyless_uam_user_creds, item_name, alg, user_metadata, split_level, **kwargs):
        # type: (str, str, CryptoAlgorithm, str, int, dict) -> None
        if not alg.is_aes():
            raise ValueError("Invalid algorithm")
        return self.uam_api.create_item(akeyless_uam_user_creds, item_name, alg.alg_name,
                                        user_metadata, split_level, **kwargs)

    def get_item(self, akeyless_uam_user_creds, item_name, **kwargs):
        # type: (str, str, dict) -> GetItemReplyObj
        return self.uam_api.get_item(akeyless_uam_user_creds, item_name, **kwargs)

    def get_user_items(self, akeyless_uam_user_creds, **kwargs):
        # type: (str, dict) -> GetUserItemsReplyObj
        return self.uam_api.get_user_items(akeyless_uam_user_creds, **kwargs)

    def update_item(self, akeyless_uam_user_creds, new_item_name, item_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.update_item(akeyless_uam_user_creds, new_item_name, item_name, **kwargs)

    def delete_item(self, akeyless_uam_user_creds, item_name, **kwargs):
        # type: (str, str, dict) -> None
        return self.uam_api.delete_item(akeyless_uam_user_creds, item_name, **kwargs)

    def create_user(self, akeyless_uam_user_creds, akeyless_set_user_access_policy_creds, user_name, **kwargs):
        # type: (str, str, str, dict) -> CreateUserReplyObj
        return self.uam_api.create_user(akeyless_uam_user_creds,
                                        akeyless_set_user_access_policy_creds,
                                        user_name, **kwargs)

    def get_user(self, akeyless_uam_user_creds, user_name, **kwargs):
        # type: (str, str, dict) -> GetUserReplyObj
        return self.uam_api.get_user(akeyless_uam_user_creds, user_name, **kwargs)

    def update_user(self, akeyless_uam_user_creds, akeyless_set_user_access_policy_creds,
                    new_user_name, user_name, **kwargs):
        # type: (str, str, str, str, dict) -> None
        return self.uam_api.update_user(akeyless_uam_user_creds, akeyless_set_user_access_policy_creds,
                                        new_user_name, user_name, **kwargs)

    def delete_user(self, akeyless_uam_user_creds, user_name, **kwargs):
        # type: (str, str, dict) -> None
        return self.uam_api.delete_user(akeyless_uam_user_creds, user_name, **kwargs)

    def create_role(self, akeyless_uam_user_creds, role_name, **kwargs):
        # type: (str, str, dict) -> None
        return self.uam_api.create_role(akeyless_uam_user_creds, role_name, **kwargs)

    def get_role(self, akeyless_uam_user_creds, role_name, **kwargs):
        # type: (str, str, dict) -> GetRoleReplyObj
        return self.uam_api.get_role(akeyless_uam_user_creds, role_name, **kwargs)

    def update_role(self, akeyless_uam_user_creds, new_role_name, role_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.update_role(akeyless_uam_user_creds, new_role_name, role_name, **kwargs)

    def delete_role(self, akeyless_uam_user_creds, role_name, **kwargs):
        # type: (str, str, dict) -> None
        return self.uam_api.delete_role(akeyless_uam_user_creds, role_name, **kwargs)

    def create_role_item_assoc(self, akeyless_uam_user_creds, role_name, associated_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.create_role_item_assoc(akeyless_uam_user_creds, role_name, associated_name, **kwargs)

    def create_role_user_assoc(self, akeyless_uam_user_creds, role_name, associated_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.create_role_user_assoc(akeyless_uam_user_creds, role_name, associated_name, **kwargs)

    def delete_role_item_assoc(self, akeyless_uam_user_creds, role_name, associated_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.delete_role_item_assoc(akeyless_uam_user_creds, role_name, associated_name, **kwargs)

    def delete_role_user_assoc(self, akeyless_uam_user_creds, role_name, associated_name, **kwargs):
        # type: (str, str, str, dict) -> None
        return self.uam_api.delete_role_user_assoc(akeyless_uam_user_creds, role_name, associated_name, **kwargs)

    def close(self):
        # type: () -> None
        self.uam_api.api_client.rest_client.pool_manager.clear()
        self.uam_api.api_client.pool.close()
        self.uam_api.api_client.pool.join()

        self.auth_api.api_client.rest_client.pool_manager.clear()
        self.auth_api.api_client.pool.close()
        self.auth_api.api_client.pool.join()

        for kfm_api in self.kfm_api_map:
            self.kfm_api_map[kfm_api].api_client.rest_client.pool_manager.clear()
            self.kfm_api_map[kfm_api].api_client.pool.close()
            self.kfm_api_map[kfm_api].api_client.pool.join()

    def _init_api_clients(self):
        # type: () -> None
        api_conf = UamApiConfiguration()
        api_conf.host = self._get_uam_host
        api_client = UamApiClient(api_conf)
        api_client.set_default_header("Cache-Control", "no-cache, no-store, must-revalidate")
        api_client.set_default_header("Pragma", "no-cache")
        api_client.set_default_header("Expires", "0")
        self.uam_api = UamApi(api_client)

        api_conf = AuthApiConfiguration()
        api_conf.host = self._get_auth_host
        api_client = AuthApiClient(api_conf)
        api_client.set_default_header("Cache-Control", "no-cache, no-store, must-revalidate")
        api_client.set_default_header("Pragma", "no-cache")
        api_client.set_default_header("Expires", "0")
        self.auth_api = AuthApi(api_client)

        self.kfm_api_map = {}

    @property
    def _get_uam_host(self):
        # type: () -> str
        return self.config.protocol + "://" + self.config.uam_server_dns

    @property
    def _get_auth_host(self):
        # type: () -> str
        return self.config.protocol + "://" + self.uam_api.get_status().auth_dns

    def _derive_key(self, derivation_creds, kfm_user_creds, derivations_data, double_derivation):
        # type: (DerivationCredsReplyObj, str, list, bool) -> (bytes, list)
        threads = []
        for i, val in derivation_creds.kf_ms_hosts_dns_map.items():
            kfm_api = self._get_kfm_api(val)
            dd = base64.b64encode(derivations_data[int(i)])
            threads.append(kfm_api.derive_fragment(kfm_user_creds, derivation_creds.credential, dd,
                                                   double_derivation=double_derivation, async=True))

        fragments = []
        derivations_data = []
        for t in threads:
            res = t.get()
            fragments.append(base64.b64decode(res.derived_fragment))
            derivations_data.append(base64.b64decode(res.derivation_data))

        return xor_fragments(fragments), derivations_data

    def _get_kfm_api(self, host):
        # type: (str) -> KfmApi

        if host in self.kfm_api_map:
            return self.kfm_api_map[host]

        api_conf = KfmApiConfiguration()
        api_conf.host = host
        api_client = KfmApiClient(api_conf)
        api_client.set_default_header("Cache-Control", "no-cache, no-store, must-revalidate")
        api_client.set_default_header("Pragma", "no-cache")
        api_client.set_default_header("Expires", "0")
        self.kfm_api_map[host] = KfmApi(api_client)
        return self.kfm_api_map[host]
