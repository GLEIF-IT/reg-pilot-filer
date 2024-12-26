import json

from keri import kering
from keri.core import MtrDex, coring, parsing
import requests

from filer.core.resolve_env import FilerEnvironment


class DigerBuilder:
    @staticmethod
    def sha256(dig):
        try:
            non_pref_dig = DigerBuilder.get_non_prefixed_digest(dig)  # Temporarily remove prefix
            non_pref_dig = bytes.fromhex(non_pref_dig)
            diger = DigerBuilder.build_diger(non_pref_dig, MtrDex.SHA2_256)
            return diger
        except Exception as e:
            raise e

    @staticmethod
    def get_non_prefixed_digest(dig):
        try:
            prefix, digest = dig.split("-", 1)
        except ValueError:
            raise kering.ValidationError(f"Digest ({dig}) must start with prefix")
        return digest

    @staticmethod
    def build_diger(raw, code):
        diger = coring.Diger(raw=raw, code=code)
        return diger


def verify_signature(signature, submitter, digest):
    env = FilerEnvironment.resolve_env()
    payload = {
        "signature": signature,
        "signer_aid": submitter,
        "non_prefixed_digest": digest
    }
    response = requests.post(f"{env.verifier_base_url}/signature/verify", json=payload)
    return response.json()

def check_login(aid):
    env = FilerEnvironment.resolve_env()
    response = requests.get(f"{env.verifier_base_url}/authorizations/{aid}")
    return response
