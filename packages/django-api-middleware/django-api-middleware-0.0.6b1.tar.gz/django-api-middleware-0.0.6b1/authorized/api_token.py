"""
================
API Token Module
================
Token handling, in charge of creating, verifying, and decoding certain token.
"""
import time

from django.conf import settings
from datetime import datetime, timedelta
import jwt
from authorized import api_utils


def generate(expiration_time=10):
    r"""
    Generates a token using the jwt library.
    The token signature requires a 'Key' that must be set in any of two places
    Project Settings or environment variable with name API_KEY
    :param expiration_time: the amount of time (in seconds) that te token will last as valid.
    :return: jwt_token value that must be appended on headers on each request.
    """
    right_now = datetime.utcnow().timestamp()
    expiration = datetime.utcnow() + timedelta(seconds=expiration_time)
    token = jwt.encode({'app_name': api_utils.get_name(),
                        'exp': int(expiration.timestamp()),
                        'iat': int(right_now),
                        'nbf': int(right_now)
                        }, api_utils.get_key(),
                       algorithm='HS512').decode('utf-8')
    return token


def verify(token):
    r"""
    Verifies a given token to match the project requirements and decoded the values.
    :param token: a token to be verified and decoded
    :return: dictionary containing a validation status and the name of the application that was placed in the payload.
    """
    response = {}
    response['is_valid'] = False
    try:
        decoded_data = jwt.decode(token,
                                api_utils.get_key(),
                                verify=True,
                                algorithms='HS512',
                                options={'verify_iat': True, 'require_exp':True, 'require_iat': True, 'require_nbf': True})
        response['is_valid'] = True
        response['app_name'] = decoded_data['app_name']
    except jwt.exceptions.InvalidSignatureError as signature_error:
        # token was signed with a non valid key.
        print('Token firmado con key diferente. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else signature_error
    except jwt.exceptions.DecodeError as decode_error:
        # token has been altered
        print('Token mal alterado. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else decode_error
    except jwt.exceptions.ExpiredSignatureError as expired_error:
        # token has expired
        print('Token expirado. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else expired_error
    except jwt.exceptions.InvalidIssuedAtError as iat_error:
        # 'issued at' claim has a future date. token has been manipulated.
        print('IAT invalido. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else iat_error
    except jwt.exceptions.MissingRequiredClaimError as missing_claim_error:
        # a claim that is required has not been sent
        print('Falta un claim. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else missing_claim_error
    except jwt.exceptions.InvalidTokenError as invalid_token_error:
        # invalid token generic exception
        print('Error general token :v. token: {}'.format(token))
        response['message'] = 'Invalid token.' if not settings.DEBUG else invalid_token_error
    return response
