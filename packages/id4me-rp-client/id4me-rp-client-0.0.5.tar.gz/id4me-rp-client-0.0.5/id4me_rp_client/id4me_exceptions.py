__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 Internet SE"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"


class ID4meException(Exception):
    pass


class ID4meDNSResolverException(ID4meException):
    pass


class ID4meDNSSECException(ID4meException):
    pass


class ID4meAuthorityConfigurationException(ID4meException):
    pass


class ID4meRelyingPartyRegistrationException(ID4meException):
    pass


class ID4meTokenRequestException(ID4meException):
    pass


class ID4meUserInfoRequestException(ID4meException):
    pass
