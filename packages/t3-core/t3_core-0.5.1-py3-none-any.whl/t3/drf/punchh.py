from requests.sessions import Session
from rest_framework.exceptions import AuthenticationFailed
import codecs
import hashlib
import hmac
import json


class PunchhSession(Session):
    """Creating our own Punchh session to perform our requests with the needed Punchh client signature header."""
    def __init__(self, base_url, secret, api_version='v1'):
        super().__init__()

        self.base_url = base_url
        self.secret = secret
        self.api_version = api_version

    def _generate_signature(self, url, r_body=None):
        uri = url.split(self.base_url)[1]
        encryption_type = hashlib.sha1
        if self.api_version == 'v2':
            encryption_type = hashlib.sha256

        if r_body:
            payload = uri + r_body
        else:
            payload = uri

        # Handling of hmac library for encryption of the header x-pch signature needed by Punchh
        new_hash = hmac.new(
            bytes(self.secret.encode('utf-8')),
            bytes(payload.encode('utf-8')),
            encryption_type).digest()

        signature = codecs.encode(new_hash, 'hex_codec')

        return signature

    def prepare_request(self, request):
        if request.data:
            request.data = json.dumps(request.data, separators=(',', ':'))
            sig = self._generate_signature(request.url, request.data)
        elif request.json:
            # TODO find out about why the json returns an invalid signature
            request.json = json.dumps(request.json, separators=(',', ':'))
            # sig = self._generate_signature(request.url, request.json)

        request.headers['Content-Type'] = 'application/json'
        request.headers['Accept'] = 'application/json'
        request.headers['x-pch-digest'] = sig

        return super().prepare_request(request)


def get_token(request, api_version='v1'):
    """Check if has token and if not, create token."""
    # Get the Authorization token from the request, if there is one.
    try:
        token = request.META['HTTP_AUTHORIZATION']
        if api_version == 'v2':
            return token.split('.')[1]
        return token.split('.')[0]
    except (KeyError, IndexError):
        raise AuthenticationFailed(f"Invalid Auth Token {api_version}.")
