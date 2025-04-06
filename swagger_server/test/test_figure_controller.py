# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.figure import Figure  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFigureController(BaseTestCase):
    """FigureController integration test stubs"""

    def test_figures_get(self):
        """Test case for figures_get

        Получить список фигурок
        """
        response = self.client.open(
            '/v1/figures',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_figures_id_delete(self):
        """Test case for figures_id_delete

        Удалить фигурку
        """
        response = self.client.open(
            '/v1/figures/{id}'.format(id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_figures_id_get(self):
        """Test case for figures_id_get

        Получить фигурку по ID
        """
        response = self.client.open(
            '/v1/figures/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_figures_id_put(self):
        """Test case for figures_id_put

        Обновить фигурку
        """
        body = Figure()
        response = self.client.open(
            '/v1/figures/{id}'.format(id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_figures_post(self):
        """Test case for figures_post

        Добавить новую фигурку
        """
        body = Figure()
        response = self.client.open(
            '/v1/figures',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
