import os
import unittest

import requests_mock

from config import TestingConfig
from frontstage import app, create_app_object
from frontstage.controllers.party_controller import notify_party_and_respondent_account_locked
from frontstage.exceptions.exceptions import ApiError
from frontstage.common.utilities import obfuscate_email
from tests.integration.mocked_services import url_get_respondent_email, url_auth_token, party, \
    url_notify_party_and_respondent_account_locked, token, url_get_conversation_count, message_count

respondent_party_id = "cd592e0f-8d07-407b-b75d-e01fbdae8233"

encoded_jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZWZyZXNoX3Rva2VuIjoiNmY5NjM0ZGEtYTI3ZS00ZDk3LWJhZjktNjN" \
                    "jOGRjY2IyN2M2IiwiYWNjZXNzX3Rva2VuIjoiMjUwMDM4YzUtM2QxOS00OGVkLThlZWMtODFmNTQyMDRjNDE1Iiwic2NvcGU" \
                    "iOlsiIl0sImV4cGlyZXNfYXQiOjE4OTM0NTk2NjEuMCwidXNlcm5hbWUiOiJ0ZXN0dXNlckBlbWFpbC5jb20iLCJyb2xlIjo" \
                    "icmVzcG9uZGVudCIsInBhcnR5X2lkIjoiZGIwMzZmZDctY2UxNy00MGMyLWE4ZmMtOTMyZTdjMjI4Mzk3In0.hh9sFpiPA-O" \
                    "8kugpDi3_GSDnxWh5rz2e5GQuBx7kmLM"

url_resend_verification_email = f'{TestingConfig.PARTY_URL}/party-api/v1/resend-verification-email' \
                                f'/{respondent_party_id}'
url_resend_verification_expired_token = f'{TestingConfig.PARTY_URL}/party-api/v1' \
                                        f'/resend-verification-email-expired-token/{token}'
get_respondent_by_id_url = f'{TestingConfig.PARTY_URL}/party-api/v1/respondents/id/{respondent_party_id}'


class TestSignIn(unittest.TestCase):
    """Test case for application endpoints and functionality"""

    def setUp(self):
        self.app = app.test_client()
        self.auth_response = {}
        self.sign_in_form = {
            "username": "testuser@email.com",
            "password": "password"
        }
        self.auth_error = {
            'detail': 'Unauthorized user credentials'
        }
        os.environ['APP_SETTINGS'] = 'TestingConfig'

    def test_view_sign_in(self):
        response = self.app.get('/sign-in/', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign in'.encode() in response.data)
        self.assertTrue('New to this service?'.encode() in response.data)

    def test_view_sign_in_from_redirect(self):
        response = self.app.get('/', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign in'.encode() in response.data)
        self.assertTrue('New to this service?'.encode() in response.data)

    def test_view_sign_in_account_activated(self):
        response = self.app.get('/sign-in?account_activated=True', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign in'.encode() in response.data)
        self.assertTrue('You\'ve activated your account'.encode() in response.data)

    def test_sign_in_no_username(self):
        del self.sign_in_form['username']

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Email Address is required'.encode() in response.data)

    def test_sign_in_invalid_username(self):
        self.sign_in_form['username'] = 'aaa'

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Invalid email address'.encode() in response.data)

    def test_sign_in_no_password(self):
        self.sign_in_form['username'] = 'testuser@email.com'
        del self.sign_in_form['password']

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Password is required'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_success(self, mock_object):
        mock_object.get(url_get_respondent_email, json=party)
        mock_object.post(url_auth_token, status_code=200, json=self.auth_response)
        mock_object.get(url_get_conversation_count, json=message_count)

        response = self.app.post('/sign-in/', data=self.sign_in_form)

        self.assertEqual(response.status_code, 302)
        self.assertTrue('/surveys/'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_success_redirect_to_url(self, mock_object):
        mock_object.get(url_get_respondent_email, json=party)
        mock_object.post(url_auth_token, status_code=200, json=self.auth_response)
        mock_object.get(url_get_conversation_count, json=message_count)
        response = self.app.post('/sign-in/', data=self.sign_in_form, query_string={'next': 'http://localhost:8082/secure-message/threads'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/secure-message/threads'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_expired_redirects_to_login_page(self, mock_object):
        mock_object.get(url_get_respondent_email, json=party)
        mock_object.post(url_auth_token, status_code=200)

        self.app.get('/sign-in/', data=self.sign_in_form)

        response = self.app.get('/surveys/todo',  follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('To help protect your information we have signed you out'.encode() in response.data)
        self.assertIn(b'Sign in', response.data)

    @requests_mock.mock()
    def test_sign_in_auth_fail(self, mock_object):
        mock_object.get(url_get_respondent_email, json=party)
        mock_object.post(url_auth_token, status_code=500)

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('An error has occurred'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_party_fail(self, mock_object):
        mock_object.get(url_get_respondent_email, status_code=500)
        mock_object.post(url_auth_token, status_code=200, json=self.auth_response)

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('An error has occurred'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_party_404(self, mock_object):
        mock_object.post(url_auth_token, status_code=204)
        mock_object.get(url_get_respondent_email, status_code=404)
        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertTrue('Incorrect email or password'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_unauthorised_auth_credentials(self, mock_object):
        mock_object.post(url_auth_token, status_code=401, json=self.auth_error)
        mock_object.get(url_get_respondent_email, json=party)

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Incorrect email or password'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_unverified_account(self, mock_object):
        self.auth_error['detail'] = 'User account not verified'
        mock_object.post(url_auth_token, status_code=401, json=self.auth_error)
        mock_object.get(url_get_respondent_email, json=party)

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please follow the link the email to confirm your email address'.encode() in response.data)
        self.assertTrue('<a href="/sign-in/resend-verification/f956e8ae-6e0f-4414-b0cf-a07c1aa3e37b">'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_unknown_response(self, mock_object):
        self.auth_error['detail'] = 'wat'
        mock_object.post(url_auth_token, status_code=401, json=self.auth_error)
        mock_object.get(url_get_respondent_email, json=party)

        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Incorrect email or password'.encode() in response.data)

    def test_logout(self):
        self.app.set_cookie('localhost', 'authorization', encoded_jwt_token)
        response = self.app.get('/sign-in/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign in'.encode() in response.data)
        self.assertTrue('New to this service?'.encode() in response.data)
        self.assertFalse('Sign out'.encode() in response.data)

    @requests_mock.mock()
    def test_resend_verification_email(self, mock_request):
        urls = ['resend_verification', 'resend-verification']
        for url in urls:
            with self.subTest(url=url):
                mock_request.get(get_respondent_by_id_url, json=party)
                mock_request.post(url_resend_verification_email, status_code=200)
                response = self.app.get(f"/sign-in/{url}/{respondent_party_id}", follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertTrue('Check your email'.encode() in response.data)

    @requests_mock.mock()
    def test_fail_resent_verification_email(self, mock_request):
        urls = ['resend_verification', 'resend-verification']
        for url in urls:
            with self.subTest(url=url):
                mock_request.post(url_resend_verification_email, status_code=500)
                response = self.app.get(f"sign-in/{url}/{respondent_party_id}",
                                        follow_redirects=True)
                self.assertEqual(response.status_code, 500)
                self.assertTrue('An error has occurred'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_account_locked(self, mock_object):
        self.auth_error['detail'] = 'User account locked'
        mock_object.post(url_auth_token, status_code=401, json=self.auth_error)
        mock_object.get(url_get_respondent_email, json=party)
        mock_object.put(url_notify_party_and_respondent_account_locked,
                        json={'respondent_id': 'f956e8ae-6e0f-4414-b0cf-a07c1aa3e37b',
                              'status_change': 'SUSPENDED',
                              'email_address': 'test@test.com'})
        response = self.app.post('/sign-in/', data=self.sign_in_form, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_notify_account_error(self, mock_object):
        self.app = create_app_object()
        self.app.testing = True
        mock_object.put(url_notify_party_and_respondent_account_locked,
                        json={'respondent_id': 'f956e8ae-6e0f-4414-b0cf-a07c1aa3e37b',
                              'status_change': 'SUSPENDED',
                              'email_address': 'test@test.com'}, status_code=500)
        with self.app.app_context():
            with self.assertRaises(ApiError):
                notify_party_and_respondent_account_locked(respondent_id='f956e8ae-6e0f-4414-b0cf-a07c1aa3e37b',
                                                           email_address='test@test.com')

    @requests_mock.mock()
    def test_resend_verification_email_using_expired_token(self, mock_object):
        mock_object.post(url_resend_verification_expired_token, status_code=200)

        response = self.app.get(f'sign-in/resend-verification-expired-token/{token}',
                                follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Check your email'.encode() in response.data)

    @requests_mock.mock()
    def test_fail_resend_verification_email_using_expired_token(self, mock_object):
        mock_object.post(url_resend_verification_expired_token, status_code=500)

        response = self.app.get(f'sign-in/resend-verification-expired-token/{token}',
                                follow_redirects=True)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('An error has occurred'.encode() in response.data)

    def test_obfuscate_email(self):
        """Tests the output of obfuscate email with both valid and invalid strings"""
        testAddresses = {
            "example@example.com": "e*****e@e*********m",
            "prefix@domain.co.uk": "p****x@d**********k",
            "first.name@place.gov.uk": "f********e@p**********k",
            "me+addition@gmail.com": "m*********n@g*******m",
            "a.b.c.someone@example.com": "a***********e@e*********m",
            "john.smith123456@londinium.ac.co.uk": "j**************6@l****************k",
            "me!?@example.com": "m**?@e*********m",
            "m@m.com": "m@m***m",
            "joe.bloggs": "j********s",
            "joe.bloggs@": "j********s",
            "@gmail.com": "@g*******m"
        }

        for test in testAddresses:
            self.assertEqual(obfuscate_email(test), testAddresses[test])
