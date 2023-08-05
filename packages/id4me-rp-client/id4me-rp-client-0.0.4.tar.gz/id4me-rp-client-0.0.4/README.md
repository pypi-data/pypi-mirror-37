# id4me-rp-client
Python Relying Party client library for ID4me protocol.
For details of the protocol, please visit: https://id4me.org

Library offers Relying Party functionality for authentication with Identity Authority and claim request from the Identity Agent..

## Specification reference
https://gitlab.com/ID4me/documentation/blob/master/id4ME%20Technical%20Specification.adoc
- Version: 1.0
- Revision: 02

## Installation
```shell
pip install id4me-rp-client
```

## Usage

### Register the client and authorize with Identity Authority

```python
from id4me_rp_client import *

# these imports are just needed in this example
from builtins import input
import json

# create client object with basic parameters of your app
client = ID4meClient(
    validate_url='https://dynamicdns.domainconnect.org/ddnscode',
    client_name='Foo app',
    logo_url='https://upload.wikimedia.org/wikipedia/commons/7/76/Foobar2000_logo_2014.png',
    policy_url='https://foo.com/policy',
    tos_url='https://foo.com/tos')


# a routine to save client registration at authority
def save_authority_registration(auth_name, auth_content):
    # Implement me...
    pass


# a routine to load client registration at authority
def load_authority_registration(auth_name):
    # Implement me...
    raise NotImplementedError('load_authority_registration not implemented')
    

try:
    # make a discovery of identity authority and register if needed
    # find_authority and save_authority are optional, but when missing client will be registered each time anew
    ctx = client.get_rp_context(
        id4me='id200.connect.domains',
        find_authority=load_authority_registration,
        save_authority=save_authority_registration)    

    # get a link to login routine
    link = client.get_consent_url(
        ctx, 
        claimsrequest=ID4meClaimsRequest(
            userinfo_claims={
                OIDCClaim.name: ID4meClaimRequestProperties(reason='To call you by name'),
                OIDCClaim.email: ID4meClaimRequestProperties(essential=True, reason='To be able to contact you'),
                OIDCClaim.email_verified: ID4meClaimRequestProperties(reason='To know if your E-mail was verified'),
            })
        )
    print('Please open the link:\n{}'.format(link))

    # Normally code will arrive as query param on client.validateUrl
    code = input('Please enter code: ')
    # Get ID token
    client.get_idtoken(context=ctx, code=code)
    # Get User Info
    userinfo = client.get_user_info(context=ctx)
    print('User Info:\n{}'.format(json.dumps(userinfo, sort_keys=True, indent=4)))    
except ID4meException as e:
    print('Exception: {}'.format(e))

```

#### Output:
```text
Resolving "_openid.id200.connect.domains."
Checking TXT record "v=OID1;iau=auth.freedom-id.de;iag=identityagent.de"
identity_authority = auth.freedom-id.de
registering with new identity authority (auth.freedom-id.de)
destination = https://auth.freedom-id.de/login?scope=openid&response_type=code&client_id=hmkzay2riyon4&redirect_uri=https%3A//foo.com/validate&login_hint=id200.connect.domains&state=&claims=%7B%22userinfo%22%3A%20%7B%22email_verified%22%3A%20%7B%22reason%22%3A%20%22To%20know%20if%20your%20E-mail%20was%20verified%22%7D%2C%20%22email%22%3A%20%7B%22reason%22%3A%20%22To%20be%20able%20to%20contact%20you%22%2C%20%22essential%22%3A%20true%7D%2C%20%22name%22%3A%20%7B%22reason%22%3A%20%22To%20call%20you%20by%20name%22%7D%7D%7D
Please open the link:
https://auth.freedom-id.de/login?scope=openid&response_type=code&client_id=hmkzay2riyon4&redirect_uri=https%3A//foo.com/validate&login_hint=id200.connect.domains&state=&claims=%7B%22userinfo%22%3A%20%7B%22email_verified%22%3A%20%7B%22reason%22%3A%20%22To%20know%20if%20your%20E-mail%20was%20verified%22%7D%2C%20%22email%22%3A%20%7B%22reason%22%3A%20%22To%20be%20able%20to%20contact%20you%22%2C%20%22essential%22%3A%20true%7D%2C%20%22name%22%3A%20%7B%22reason%22%3A%20%22To%20call%20you%20by%20name%22%7D%7D%7D
Please enter code: >? 9jNXCX9OZ4HQLr2YZWKisw.5mSDkoR-5YJQoTp3f1vuxg
User Info:
{
    "aud": "hmkzay2riyon4", 
    "email": "foo@bar.de", 
    "email_verified": true, 
    "exp": 1538762218, 
    "iat": 1538761918, 
    "id4me.identifier": "id200.connect.domains", 
    "id4me.identity": "id200.connect.domains", 
    "iss": "https://auth.freedom-id.de", 
    "nbf": 1538761918, 
    "sub": "uiw3pTRRLVaKJqbnbSwr4EVuhEPTHvRgci91RbhYU2rab/YVDqDmqTKzTVAdDMm+", 
    "updated_at": 1538564738
}
```

## TODOs
- serialization and deserialization of context for easy storage 
- usage of 