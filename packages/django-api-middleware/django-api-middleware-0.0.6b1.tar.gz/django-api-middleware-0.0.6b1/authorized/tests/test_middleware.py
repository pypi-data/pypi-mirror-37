from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from authorized.middleware import APIAuthRequestMiddleware
from mock import MagicMock
from authorized.models import Applications
from authorized import api_utils, api_token
import jwt
import time


class AuthorizedAPIMiddlewareTests(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.request.path = '/sample'
        self.request.META = {}
        self.request.session = {}
        self.get_response = None
        self.middleware = APIAuthRequestMiddleware(self.get_response)

        self.expired_token = api_token.generate(expiration_time=1)
        self.non_expired_token = api_token.generate(expiration_time=15)
        self.correct_content_type = 'application/vnd.api+json'
        Applications.objects.create(name='Dummy', can_request= True)
        Applications.objects.create(name='Random', can_request= False)

    def test_request_without_header(self):
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_expired_token(self):
        time.sleep(3)
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': self.expired_token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_request_signed_with_invalid_key(self):
        token = jwt.encode({'app_name': api_utils.get_name(),
                    'exp': datetime.utcnow() + timedelta(seconds=3),
                    'iat': datetime.utcnow(),
                    'nbf': datetime.utcnow()
                    },
                    'invalid_key',
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_missing_exp_claim(self):
        # missing exp claim
        token = jwt.encode({'app_name': api_utils.get_name(),
                    'iat': datetime.utcnow(),
                    'nbf': datetime.utcnow()
                    },
                    api_utils.get_key(),
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_missing_iat_claim(self):
        # missing iat claim
        token = jwt.encode({'app_name': api_utils.get_name(),
                    'exp': datetime.utcnow() + timedelta(seconds=3),
                    'nbf': datetime.utcnow()
                    },
                    api_utils.get_key(),
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_missing_nbf_claim(self):
        # missing nbf claim
        token = jwt.encode({'app_name': api_utils.get_name(),
                    'exp': datetime.utcnow() + timedelta(seconds=3),
                    'iat': datetime.utcnow(),
                    },
                    api_utils.get_key(),
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_no_registered_app(self):
        token = jwt.encode({'app_name': 'MRNOBODY',
                    'exp': datetime.utcnow() + timedelta(seconds=2),
                    'iat': datetime.utcnow(),
                    'nbf': datetime.utcnow()
                    },
                    api_utils.get_key(),
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_app_with_no_permission(self):
        token = jwt.encode({'app_name': 'Random',
                    'exp': datetime.utcnow() + timedelta(seconds=2),
                    'iat': datetime.utcnow(),
                    'nbf': datetime.utcnow()
                    },
                    api_utils.get_key(),
                    algorithm='HS512').decode('utf-8')
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_with_valid_token(self):
        url = reverse('non_third_party_sample-list')
        response = APIClient().post(url, content_type=self.correct_content_type, **{'HTTP_APPLICATION_TOKEN': self.non_expired_token})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)