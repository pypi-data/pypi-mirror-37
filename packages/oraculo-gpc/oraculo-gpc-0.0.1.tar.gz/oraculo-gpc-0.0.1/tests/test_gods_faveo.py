#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `oraculo` package."""
import unittest
from mock import patch, MagicMock
from oraculo.gods import faveo, exceptions


class TestAPIClient(unittest.TestCase):

    def test_initial_attribute(self):
        # WHEN
        client = faveo.APIClient

        # THEN
        self.assertEqual(client._authenticated, False)
        self.assertEqual(
            client.base_url, 'http://faveo.grupopuntacana.com:81/')
        _authenticate_url = client.base_url + 'api/v1/authenticate'
        self.assertEqual(client._authenticate_url, _authenticate_url)

    def test_success_authentication(self):
        # WHEN
        instance_client = faveo.APIClient()

        # THEN
        self.assertEqual(instance_client._authenticated, True)

    @patch('oraculo.gods.faveo.requests.post')
    def test_invalid_authentication(self, mock_get):
        # GIVEN
        response = MagicMock()
        response.status_code = 403
        mock_get.return_value = response

        # THEN
        self.assertRaises(faveo.CantAuthenticate, faveo.APIClient)

    @patch('oraculo.gods.faveo.requests.get')
    def test_get_status_code_ok(self, mock_get):
        # GIVEN
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = dict(data=dict())
        mock_get.return_value = response

        # WHEN
        client = faveo.APIClient()
        result = client.get('test')

        # THEN
        self.assertIsInstance(result, dict)

    @patch('oraculo.gods.faveo.requests.get')
    def test_get_status_code_not_found(self, mock_get):
        # GIVEN
        response = MagicMock()
        response.status_code = 404
        mock_get.return_value = response
        client = faveo.APIClient()

        # THEN
        self.assertRaises(exceptions.NotFound, client.get('test'))

    @patch('oraculo.gods.faveo.requests.post')
    def test_post_status_code_ok(self, mock_post):
        # GIVEN
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = dict(data=dict())
        mock_post.return_value = response

        # WHEN
        client = faveo.APIClient()
        result = client.post('test', {})

        # THEN
        self.assertIsInstance(result, dict)

    @patch('oraculo.gods.faveo.requests.post')
    def test_post_status_code_not_found(self, mock_post):
        # GIVEN
        response = MagicMock()
        response.status_code = 404
        mock_post.return_value = response
        client = faveo.APIClient()

        # THEN
        self.assertRaises(exceptions.NotFound, client.post, 'test', {})
