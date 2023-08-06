# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zforeach.py
   Author :       Zhang Fan
   date：         18/10/31
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'


class _discard_foreach_data:
    pass


class foreach_object():
    def __init__(self, value, main_type: type, main_type_text: str, level=None, key=None):
        assert main_type, '请设置main_type'
        assert main_type_text, '请设置main_type_text'

        self._value = value
        self._value_type_text = None

        self._main_type = main_type
        self._main_type_text = main_type_text
        self._level = level or 1
        self._key = key
        self._is_discard = False
        self._retry_deep_foreach = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data):
        self.set_value(data)

    @property
    def main_type(self):
        return self._main_type

    @property
    def main_type_text(self):
        return self._main_type_text

    @property
    def level(self):
        return self._level

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, data):
        assert self.main_type is dict, '只有dict才存在key属性'
        self._key = data

    @property
    def value_type_text(self):
        if self._value_type_text is None:
            self._value_type_text = get_base_type_text_of_value(self._value)
        return self._value_type_text

    def is_base_data_type(self):
        return self.value_type_text

    def is_main_type(self):
        return self.value_type_text == self._main_type_text

    def is_discard(self):
        return self._is_discard or (self.value is _discard_foreach_data)

    def is_retry_deep_foreach(self):
        return self._retry_deep_foreach

    def set_value(self, data):
        self._value = data
        self._value_type_text = None

    def discard(self):
        self._is_discard = True

    def retry_deep_foreach(self):
        self._retry_deep_foreach = True

    def __str__(self):
        if self._key:
            return '<level:{}> {}: {}'.format(self._level, self._key, self._value)

        return '<level:{}> {}'.format(self._level, self._value)


def get_base_type_text_of_value(value):
    if isinstance(value, dict):
        return 'dict'
    if isinstance(value, list):
        return 'list'
    if isinstance(value, tuple):
        return 'tuple'
    if isinstance(value, set):
        return 'set'


def get_base_type_text_of_type(main_type: type):
    if issubclass(main_type, dict):
        return 'dict'
    if issubclass(main_type, list):
        return 'list'
    if issubclass(main_type, tuple):
        return 'tuple'
    if issubclass(main_type, set):
        return 'set'


def get_base_type_of_type_text(type_text: str):
    if type_text == 'dict':
        return dict
    if type_text == 'list':
        return list
    if type_text == 'tuple':
        return tuple
    if type_text == 'set':
        return set


def get_base_type_of_value(value):
    main_type = type(value)
    if issubclass(main_type, dict):
        return dict
    if issubclass(main_type, list):
        return list
    if issubclass(main_type, tuple):
        return tuple
    if issubclass(main_type, set):
        return set


def _value_transform(item: foreach_object, callback, deep=False, allow_other_type=False):
    if item.is_discard():
        return _discard_foreach_data

    if not deep or not item.is_base_data_type():
        callback(item)

        if item.is_discard():
            return _discard_foreach_data

        if item.is_retry_deep_foreach() and item.is_base_data_type() and item.value:
            item._retry_deep_foreach = False
            return _value_transform(item, callback=callback, deep=deep, allow_other_type=allow_other_type)

        return item.value

    return _deep_value_transform(item, callback=callback, allow_other_type=allow_other_type)


def _deep_value_transform(item: foreach_object, callback, allow_other_type=False):
    if allow_other_type:
        item.value = foreach_data(item.value, callback=callback, deep=True, level=item.level + 1)
        callback(item)
    elif item.is_main_type():
        func_name = 'foreach_{}'.format(item.main_type_text)
        foreach_func = globals().get(func_name)
        # assert foreach_func, '未定义函数: {}'.format(func_name)
        item.value = foreach_func(item.value, callback=callback, deep=True, allow_other_type=allow_other_type,
                                  level=item.level + 1)
        callback(item)
    else:
        return item.value

    if item.is_discard():
        return _discard_foreach_data

    if item.is_retry_deep_foreach() and item.is_base_data_type() and item.value:
        item._retry_deep_foreach = False
        return _deep_value_transform(item, callback=callback, allow_other_type=allow_other_type)

    return item.value


def foreach_data(data: dict or list or tuple or list, callback, deep=False, level=None):
    value_type_text = get_base_type_text_of_value(data)
    assert value_type_text, '只能传入dict, list, tuple, list, 你传入的是: {}'.format(type(data))

    func_name = 'foreach_{}'.format(value_type_text)
    foreach_func = globals().get(func_name)
    # assert foreach_func, '未定义函数: {}'.format(func_name)
    return foreach_func(data, callback=callback, deep=deep, allow_other_type=True, level=level)


def foreach_dict(data: dict, callback, deep=False, allow_other_type=False, level=None):
    assert isinstance(data, dict), '只能传入dict, 你传入的是: {}'.format(type(data))
    result_item = dict()
    for key, value in data.items():
        item = foreach_object(value, main_type=dict, main_type_text='dict', level=level, key=key)
        value = _value_transform(item, callback=callback, deep=deep, allow_other_type=allow_other_type)

        if value is _discard_foreach_data:
            continue

        result_item[item.key] = value
    return result_item


def _foreach_iter(data, main_type: list or tuple or set, callback, deep=False, allow_other_type=False, level=None):
    main_type_text = get_base_type_text_of_type(main_type)
    assert isinstance(data, main_type), '只能传入{}, 你传入的是: {}'.format(main_type_text, type(data))
    result_item = []
    for value in data:
        item = foreach_object(value, main_type=main_type, main_type_text=main_type_text, level=level)
        value = _value_transform(item, callback=callback, deep=deep, allow_other_type=allow_other_type)

        if value is _discard_foreach_data:
            continue

        result_item.append(value)

    if main_type is list:
        return result_item

    return main_type(result_item)


def foreach_list(data: list, callback, deep=False, allow_other_type=False, level=None):
    return _foreach_iter(data, main_type=list, callback=callback, deep=deep, allow_other_type=allow_other_type,
                         level=level)


def foreach_tuple(data: tuple, callback, deep=False, allow_other_type=False, level=None):
    return _foreach_iter(data, main_type=tuple, callback=callback, deep=deep, allow_other_type=allow_other_type,
                         level=level)


def foreach_set(data: set, callback, deep=False, allow_other_type=False, level=None):
    return _foreach_iter(data, main_type=set, callback=callback, deep=deep, allow_other_type=allow_other_type,
                         level=level)


if __name__ == '__main__':
    def foreach_fun(item: foreach_object):
        print('foreach:', item)
        if item.key == 'level2':
            item.key = 'change_level2'


    data = [
        'level1',
        {
            'level2':
                [
                    'level3'
                ],
        }
    ]

    value = foreach_data(data, foreach_fun, deep=True)
    print('结果', value)
