__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 Internet SE"
__credits__ = ["Andreea Dima", "Marc Laue"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"

import json
import datetime
import logging
from uuid import uuid4

from jwcrypto.common import JWException
from six.moves import urllib

from .network import get_json_auth, post_json, post_data, NetworkContext, http_request
from .id4me_exceptions import *
from dns.exception import Timeout
from dns.resolver import Resolver, NXDOMAIN, YXDOMAIN, NoAnswer, NoNameservers
from dns.message import make_query
import dns.name
import dns.dnssec
from .stringify_keys import stringify_keys
from jwcrypto import jwt, jwk, jwe

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

resolver = Resolver()

jws_alg_map = {
    "HS256": "oct",
    "HS384": "oct",
    "HS512": "oct",
    "RS256": "RSA",
    "RS384": "RSA",
    "RS512": "RSA",
    "ES256": "ES",
    "ES384": "ES",
    "ES512": "ES",
}


class ID4meContext(object):
    def __init__(self, id4me, identity_authority, registration):
        """
        :type registration: dict
        :type identity_authority: str
        """
        self.id = id4me
        self.iau = identity_authority
        self.client_id = registration['client_id']
        self.client_secret = registration['client_secret']
        if 'private_jwks' in registration:
            self.private_jwks = registration['private_jwks']
        self.access_token = None
        self.refresh_token = None
        self.iss = None
        self.sub = None

    @staticmethod
    def _serialize_priv_keys(registration):
        if 'private_jwks' in registration:
            prvkeys = registration['private_jwks']
            del registration['private_jwks']
            registration['private_jwks_enc'] = prvkeys.export()

    @staticmethod
    def _deserialize_priv_keys(registration):
        if 'private_jwks_enc' in registration:
            registration['private_jwks'] = jwk.JWKSet.from_json(registration['private_jwks_enc'])
            del registration['private_jwks_enc']

    def to_json(self):
        try:
            if self.private_jwks:
                self.private_jwks_enc = self.private_jwks.export()
                del self.private_jwks
            return json.dumps(self, default=lambda o: o.__dict__)
        finally:
            if self.private_jwks_enc:
                self.private_jwks = jwk.JWKSet.from_json(self.private_jwks_enc)
            del self.private_jwks_enc

    @staticmethod
    def from_json(json_string):
        jsonobj = json.loads(json_string)
        ctx = ID4meContext(
            id4me=jsonobj['id'],
            identity_authority=jsonobj['iau'],
            registration=jsonobj
        )
        if 'private_jwks_enc' in jsonobj:
            ctx.private_jwks = jwk.JWKSet.from_json(jsonobj['private_jwks_enc'])
        ctx.access_token = jsonobj.get('access_token', None)
        ctx.refresh_token = jsonobj.get('refresh_token', None)
        ctx.iss = jsonobj.get('iss', None)
        ctx.sub = jsonobj.get('sub', None)
        return ctx

class ID4meClaimsRequest(object):
    def __init__(self, id_token_claims=None, userinfo_claims=None):
        if id_token_claims is not None:
            self.id_token = id_token_claims
        if userinfo_claims is not None:
            self.userinfo = userinfo_claims


class ID4meClaimRequestProperties(object):
    def __init__(self, essential=None, reason=None):
        if essential is not None:
            self.essential = essential
        if reason is not None:
            self.reason = reason


class ID4meClient(object):
    def __init__(self, validate_url,
                 jwks_url=None,
                 app_type=None,
                 client_name=None,
                 preferred_client_id=None,
                 logo_url=None,
                 policy_url=None,
                 tos_url=None,
                 private_jwks=None,
                 network_context=None,
                 requireencryption=None):
        self.validateUrl = validate_url
        self.jwksUrl = jwks_url
        self.client_name = client_name
        self.preferred_client_id = preferred_client_id
        self.logoUrl = logo_url
        self.policyUrl = policy_url
        self.tosUrl = tos_url
        self.private_jwks = private_jwks
        self.requireencryption = requireencryption

        if network_context is not None:
            self.networkContext = network_context
        else:
            self.networkContext = NetworkContext()
        self.app_type = app_type

    @staticmethod
    def _get_identity_authority(id4me):
        hostname = '_openid.{}.'.format(id4me)
        logger.debug('Resolving "{}"'.format(hostname))
        try:
            dns_resolver = resolver.query(hostname, 'TXT')
            # TODO: enforce strict DNSSEC policy when support added by all parties...
            # self._check_dns_sec(id)
            for txt in dns_resolver:
                value = str(txt).replace('"', '')
                logger.debug('Checking TXT record "{}"'.format(value))
                if not value.startswith('v=OID1;'):
                    continue
                for item in value.split(';'):
                    if item.startswith('iau=') or item.startswith('iss='):
                        return item[4:]
        except Timeout:
            logger.debug('Timeout. Failed to resolve "{}"'.format(hostname))
            raise ID4meDNSResolverException('Timeout. Failed to resolve "{}"'.format(hostname))
        except NXDOMAIN or YXDOMAIN:
            logger.debug('Failed to resolve "{}"'.format(hostname))
            raise ID4meDNSResolverException('Failed to resolve "{}"'.format(hostname))
        except NoAnswer:
            logger.debug('Failed to find TXT records for "{}"'.format(hostname))
            raise ID4meDNSResolverException('Failed to find TXT records for "{}"'.format(hostname))
        except NoNameservers:
            logger.debug('No nameservers avalaible to dig "{}"'.format(hostname))
            raise ID4meDNSResolverException('No nameservers avalaible to dig "{}"'.format(hostname))
            logger.debug('No suitable TXT DNS entry found for {}'.format(id4me))
        raise ID4meDNSResolverException('No suitable TXT DNS entry found for {}'.format(id4me))

    def _get_openid_configuration(self, issuer):
        try:
            url = '{}{}/.well-known/openid-configuration'.format(
                '' if issuer.startswith('https://') else 'https://',
                issuer)
            return get_json_auth(self.networkContext, url)
        except Exception as e:
            logger.warn(e)
            raise ID4meAuthorityConfigurationException('Could not get configuration for {}'.format(issuer))

    @staticmethod
    def _check_dns_sec(domain):
        try:
            domain_authority = resolver.query(domain, 'SOA')
            response = resolver.query(domain_authority, 'NS')
            nsname = response.rrset[0]
            response = resolver.query(nsname, 'A')
            nsaddr = response.rrset[0].to_text()
            # noinspection PyTypeChecker
            request = make_query(domain, 'DNSKEY', want_dnssec=True)
            # noinspection PyUnresolvedReferences
            response = resolver.query.udp(request, nsaddr)
            if response.rcode() != 0:
                logger.debug('No DNSKEY record found for {}'.format(domain))
                raise ID4meDNSSECException('No DNSKEY record found for {}'.format(domain))
            else:
                answer = response.answer
                if len(answer) != 2:
                    logger.warn('DNSSEC check failed for {}'.format(domain))
                    raise ID4meDNSSECException('DNSSEC check failed for {}'.format(domain))
                else:
                    name = dns.name.from_text(domain)
                    try:
                        dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
                        logger.debug('DNS response for "{}" is signed.'.format(domain))
                    except dns.dnssec.ValidationFailure:
                        logger.warn('DNS response for "{}" is insecure. Trusting it anyway'.format(domain))
                        raise ID4meDNSSECException(
                            'DNS response for "{}" is insecure. Trusting it anyway'.format(domain))
        except Exception:
            logger.debug('DNSSEC check failed for {}'.format(domain))
            raise ID4meDNSSECException('DNSSEC check failed for {}'.format(domain))

    @staticmethod
    def _generate_new_private_keys_set():
        key = jwk.JWK(generate='RSA', size=2048, kid=str(uuid4()))
        kset = jwk.JWKSet()
        kset.add(key)
        return kset

    def _register_identity_authority(self, identity_authority):
        identity_authority_config = self._get_openid_configuration(identity_authority)
        logger.info('registering with new identity authority ({})'.format(identity_authority))
        # TODO: generate jwks only when no jwks URL provided (and then find a way to have private keys available here
        # for decryption)
        jwks = self.private_jwks if self.private_jwks is not None else self._generate_new_private_keys_set()

        if 'RS256' not in identity_authority_config['id_token_signing_alg_values_supported']:
            raise ID4meRelyingPartyRegistrationException(
                'Required signature algorithm for id_token RS256 not supported by Authority')
        if 'RS256' not in identity_authority_config['userinfo_signing_alg_values_supported']:
            raise ID4meRelyingPartyRegistrationException(
                'Required signature algorithm for userinfo RS256 not supported by Authority')

        request = {
            'redirect_uris': ['{}'.format(self.validateUrl)],
            'id_token_signed_response_alg': 'RS256',
            'userinfo_signed_response_alg': 'RS256',
            # TODO: only send jwks if no jwks_uri
            'jwks': json.loads(jwks.export(private_keys=False))
        }

        if self.requireencryption or self.requireencryption is None:
            if 'RSA-OAEP-256' not in identity_authority_config['id_token_encryption_alg_values_supported']:
                raise ID4meRelyingPartyRegistrationException(
                    'Required encryption algorithm for id_token RSA-OAEP-256 not supported by Authority')
            if 'RSA-OAEP-256' not in identity_authority_config['userinfo_encryption_alg_values_supported']:
                raise ID4meRelyingPartyRegistrationException(
                    'Required encryption algorithm for userinfo RSA-OAEP-256 not supported by Authority')
            request['id_token_encrypted_response_alg'] = 'RSA-OAEP-256'
            request['userinfo_encrypted_response_alg'] = 'RSA-OAEP-256'

        if self.preferred_client_id is not None:
            request['preferred_client_id'] = self.preferred_client_id
        if self.client_name is not None:
            request['client_name'] = self.client_name
        if self.logoUrl is not None:
            request['logo_uri'] = self.logoUrl
        if self.policyUrl is not None:
            request['policy_uri'] = self.policyUrl
        if self.tosUrl is not None:
            request['tos_uri'] = self.tosUrl

        if self.app_type is not None:
            request['application_type'] = str(self.app_type)
        try:
            registration = json.loads(
                post_json(
                    self.networkContext,
                    identity_authority_config['registration_endpoint'],
                    request)
            )
            registration['private_jwks'] = jwks
        except Exception:
            raise ID4meRelyingPartyRegistrationException('Could not register {}'.format(identity_authority))
        return registration

    def get_rp_context(self, id4me, find_authority=None, save_authority=None):
        """
        Makes discovery of ID4me identifier id4me. Performs registration at relevant authority,
        if necessary or recalls a saved authority data via a callback
        :param str id4me: ID4me identifier
        :param fun(str)->str find_authority: callback to lookup authority registration - params - name, ret - value
        :param fun(str, str)->None save_authority: callback to save authority settings - params - name, value
        :return: context of ID to use with other flows
        :rtype: ID4meContext
        :raises ID4meRelyingPartyRegistrationException: in case of issues with registration
        """
        identity_authority = self._get_identity_authority(id4me)
        logger.debug('identity_authority = {}'.format(identity_authority))
        registration = None
        if find_authority is not None:
            # noinspection PyBroadException
            try:
                registration = json.loads(find_authority(identity_authority))
                ID4meContext._deserialize_priv_keys(registration)
            except Exception:
                # ignore all exceptions (we'll try to re-register as fallback
                pass
        if registration is None:
            registration = self._register_identity_authority(identity_authority)
            if save_authority is not None:
                try:
                    ID4meContext._serialize_priv_keys(registration)
                    save_authority(identity_authority, json.dumps(registration))
                finally:
                    ID4meContext._deserialize_priv_keys(registration)

        context = ID4meContext(id4me=id4me,
                               identity_authority=identity_authority,
                               registration=registration)
        return context

    def get_consent_url(self, context, state='', claimsrequest=None, prompt=None):
        # TODO: document input parameters
        auth_config = self._get_openid_configuration(context.iau)

        endpoint = '{}'.format(self.validateUrl)
        destination = '{}?scope=openid&response_type=code&client_id={}&redirect_uri={}' \
                      '&login_hint={}&state={}'.format(
                            auth_config['authorization_endpoint'],
                            urllib.parse.quote(context.client_id),
                            urllib.parse.quote(endpoint),
                            urllib.parse.quote(context.id),
                            urllib.parse.quote(state)
                      )

        if prompt is not None:
            destination = '{}&prompt={}'.format(
                destination,
                urllib.parse.quote(str(prompt))
            )

        if claimsrequest is not None:
            claims = json.dumps(stringify_keys(claimsrequest), default=lambda o: o.__dict__)
            destination = '{}&claims={}'.format(
                destination,
                urllib.parse.quote(claims)
            )

        logger.debug('destination = {}'.format(destination))
        return destination

    def get_idtoken(self, context, code):
        # TODO: document input parameters
        auth_config = self._get_openid_configuration(context.iau)
        data = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(
            code, self.validateUrl)
        try:
            response = json.loads(
                post_data(
                    self.networkContext,
                    auth_config['token_endpoint'],
                    data,
                    basic_auth=(context.client_id, context.client_secret)
                )
            )
        except Exception as e:
            raise ID4meTokenRequestException(
                'Failed to get authorization token from {} ({})'.format(context.iau, e))
        if 'access_token' in response and 'token_type' in response and response['token_type'] == 'Bearer':
            context.access_token = response['access_token']
            # TODO: access_token is a JWS, not JWE. Too much disclosure?
            # to enable encryption we need different access_tokens for each distributed claims provider
            # (encrypted with their public keys)
            decoded_token = self._decode_token(context.access_token, context, context.iau, verify_aud=False)
            context.iss = decoded_token['iss']
            context.sub = decoded_token['sub']
        else:
            raise ID4meTokenRequestException('Access token missing in authority token response')
        if 'refresh_token' in response:
            context.refresh_token = response['refresh_token']
        if 'id_token' in response:
            payload = self._decode_token(response['id_token'], context, context.iau)
            return payload
        else:
            raise ID4meTokenRequestException('ID token missing in authority token response')

    def get_user_info(self, context):
        # TODO: document input parameters
        if context.access_token is None:
            raise ID4meUserInfoRequestException('No access token is session. Call id_token() first.')
        # TODO: we need to check access token for expiry and renew with refresh_token if expired (and avail.)
        auth_config = self._get_openid_configuration(context.iau)
        try:
            response, _ = http_request(
                context=self.networkContext,
                method='GET',
                url=auth_config['userinfo_endpoint'],
                bearer=context.access_token
            )
        except Exception as e:
            raise ID4meTokenRequestException(
                'Failed to get user info from {} ({})'.format(context.userinfo_endpoint, e.message))
        user_claims = {
            'iss': context.iss,
            'sub': context.sub
        }
        self._decode_user_info(context, response, user_claims, context.iss)
        return user_claims

    def _get_distributed_claims(self, context, endpoint, access_code, user_claims):
        try:
            response, status = http_request(
                context=self.networkContext,
                url=endpoint,
                method='GET',
                bearer=access_code,
            )
            if status == 200:
                # we need to assume iss from endpoint
                url = urllib.parse.urlparse(endpoint)
                iss = '{}://{}/'.format(url.scheme, url.netloc)
                # TODO: seems that distributed claims just come as JWT, not JWE
                # TODO: need to figure out how client's public keys are to be passed down to agent
                self._decode_user_info(context, response, user_claims, iss)
            else:
                raise ID4meTokenRequestException('Wrong status: {}'.format(status))
        except Exception as e:
            raise ID4meTokenRequestException(
                'Failed to get distributed user info from {} ({})'.format(endpoint, e.message))
        return

    def _decode_token(self, token, context, iss, leeway=datetime.timedelta(minutes=5), verify_aud=True):
        tokenproc = jwt.JWT()
        tokenproc.leeway = leeway.total_seconds()
        # first deserialize without key to get to the header (and detect type)
        tokenproc.deserialize(token)

        encryptionused = False
        if isinstance(tokenproc.token, jwe.JWE):
            # if it's JWE, decrypt with private key first
            tokenproc.deserialize(token, context.private_jwks)
            encryptionused = True
            token = tokenproc.claims

        if self.requireencryption and not encryptionused:
            raise ID4meTokenRequestException('Token does not use encryption when required')

        issuer_config = self._get_openid_configuration(iss)
        keys = self._get_public_keys_set(issuer_config['jwks_uri'])
        try:
            # we need to check if there is key id in the header (otherwise we need a try all matching keys...)
            # TODO: clarify why Agent does not set kid as workaround seems clunky
            head = tokenproc.token.jose_header
            if 'kid' not in head and 'alg' in head and head['alg'] in jws_alg_map:
                success = False
                for k in keys:
                    if (k.get_op_key('verify') is not None) and k.key_type == jws_alg_map[head['alg']]:
                        try:
                            tokenproc.deserialize(token, k)
                            success = True
                            break
                        except (JWException, RuntimeError, ValueError):
                            # trial and error...
                            pass
                if not success:
                    raise ID4meTokenRequestException("None of keys is able to verify signature")
            else:
                tokenproc.deserialize(token, keys)
        except JWException as ex:
            raise ID4meTokenRequestException("Cannot decode token: {}".format(ex))

        try:
            payload = json.loads(tokenproc.claims)
        except ValueError as ex:
            raise ID4meTokenRequestException("Cannot decode claims content: {}".format(ex))

        if 'id4me.identifier' in payload and context.id != payload['id4me.identifier']:
            logger.warn('Id4me mismatch in token')
            raise ID4meTokenRequestException(
                'Identifier mismatch in token. Requested: {}, Received: {}'.format(context.id,
                                                                                   payload['id4me.identifier']))
        if context.sub is not None and context.sub != payload['sub']:
            logger.warn('sub mismatch in token')
            raise ID4meTokenRequestException('sub mismatch in token')
        if verify_aud and payload['aud'] != context.client_id:
            logger.warn('aud mismatch in token')
            raise ID4meTokenRequestException('aud mismatch in token')
        if 'azp' in payload and payload['azp'] != context.client_id:
            logger.warn('azp mismatch in token')
            raise ID4meTokenRequestException('azp mismatch in token')
        return payload

    def _get_public_keys_set(self, jwks_uri):
        try:
            jwks, _ = http_request(self.networkContext, method='GET', url=jwks_uri)
            ret = jwk.JWKSet.from_json(jwks)
        except Exception as ex:
            raise ID4meAuthorityConfigurationException('Could not get public keys for {}, {}'.format(jwks_uri, ex))
        return ret

    def _decode_user_info(self, context, jwtresponse, user_claims, iss, leeway=datetime.timedelta(minutes=5)):
        response = self._decode_token(jwtresponse, context, iss, leeway)

        queried_endpoints = {}
        if '_claim_sources' in response and '_claim_names' in response:
            for claimref in response['_claim_names']:
                if response['_claim_names'][claimref] in response['_claim_sources'] \
                        and 'access_token' in response['_claim_sources'][response['_claim_names'][claimref]] \
                        and 'endpoint' in response['_claim_sources'][response['_claim_names'][claimref]]:
                    endpoint = response['_claim_sources'][response['_claim_names'][claimref]]['endpoint']
                    access_token = response['_claim_sources'][response['_claim_names'][claimref]]['access_token']
                    if (endpoint, access_token) not in queried_endpoints:
                        self._get_distributed_claims(context, endpoint, access_token, user_claims)
                        queried_endpoints[(endpoint, access_token)] = True
        for key in response:
            if key != '_claim_sources' and key != '_claim_names' and key not in user_claims:
                user_claims[key] = response[key]
