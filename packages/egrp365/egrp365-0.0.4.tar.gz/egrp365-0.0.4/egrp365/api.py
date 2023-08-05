# -*- coding: utf-8 -*-
"""
egrp365.api module.

Клиент API https://egrp365.ru для получения данных из ЕГРН Росреестра.

:copyright: (c) 2018 by egrp365.ru
:license: MIT, see LICENSE for more details.
"""

import requests
import re


class EgrpException(Exception):
    pass


class EGRP365:
    """
    Клиент API https://egrp365.ru для получения данных из ЕГРН Росреестра.

    :param api_key: Api key
    """
    _base_url = 'https://egrp365.ru/api/v2/'
    _api_key = ''

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def _send(self, request_type: str, method: str, params=None) -> dict:
        """
        :param request_type:
        :param method:
        :param params:
        :return:
        """
        if params is None:
            params = {}
        try:
            request_params = {'apiKey': self._api_key}
            request_params.update(params)

            response = getattr(requests, request_type)(self._base_url + method, params=request_params)

            if response.status_code != 200:
                raise EgrpException('Ошибка получения данных')

            json = response.json()
            if isinstance(json, dict) and json.get('error') and len(json.get('error')) == 2:
                raise EgrpException(json.get('error')[1])

            if isinstance(json, list) and len(json) == 0:
                raise EgrpException('Ничего не найдено')

            return json
        except EgrpException as e:
            return {'error': str(e)}

    def _check_required(self, required_fields: tuple, params_fields: tuple):
        """
        :param required_fields:
        :param params_fields:
        :return:
        """
        error_fields = frozenset(required_fields).difference(params_fields)
        if len(error_fields) != 0:
            raise EgrpException('Отсутствуют обязательные поля: ' + ', '.join(error_fields))

    def get_docs(self) -> dict:
        """
        Возвращает список доступных для заказа документов.
        """
        return self._send('get', 'getDocs')

    def get_objects_by_kadnum(self, kadnum: str, reestr='') -> dict:
        """
        Возвращает список объектов по указанному кадастровому/условному номеру.

        :param kadnum:
        :param reestr:
        :return:
        """
        params = {'kadnum': kadnum, 'reestr': reestr}
        return self._send('get', 'getObjectsByKadnum', params)

    def get_objects_by_address(self, params: dict) -> dict:
        """
        Возвращает список объектов по указанному адресу

        :param params:
        :return: dict
        """
        required_fields = 'region', 'street', 'house'
        params_fields = tuple(params.keys())
        self._check_required(required_fields, params_fields)
        return self._send('get', 'getObjectsByAddress', params)

    def get_info_by_object_id(self, object_id: str):
        """
        Возвращает информацию по указанному id объекта.

        :param object_id:
        :return:
        """
        if re.match(r'^([0-9\-:/ _*]+)$', object_id) is None:
            raise EgrpException('Неверный формат id объекта')
        return self._send('get', 'getInfoByObjectId', {'objectid': object_id})

    def post_order(self, params: dict):
        """
        Отправляет запрос на получение документов из Росреестра по указанному объекту,
        возвращает номер заказа и ссылку на оплату.

        :param params:
        :return:
        """
        required_fields = 'kadnum', 'objectid', 'email', 'phone'
        params_fields = tuple(params.keys())
        self._check_required(required_fields, params_fields)

        if re.match(r'^([0-9\-:/ _*]+)$', params.get('objectid')) is None:
            raise EgrpException('Неверный формат id объекта')

        if re.match(r'^([0-9\-:/ _*]+)$', params.get('kadnum')) is None:
            raise EgrpException('Неверный формат кадастрового номера')

        return self._send('post', 'postOrder', params)

    def get_order_status(self, order_id: str, email: str):
        """
        Возвращает статусы по каждому документу указанного заказа.

        :param order_id:
        :param email:
        :return:
        """
        params = {
            'orderid': order_id,
            'email': email
        }
        return self._send('get', 'getOrderStatus', params)
