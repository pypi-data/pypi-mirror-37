#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `uricache` package."""

from os import path, remove
from unittest import TestCase, main
from uricache import URICache


class TestURICache(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.defaults = {
            'level1': {
                'a1': 'A1',
                'level2': {
                    'a2': 'A2',
                    'level3': {
                        'a3': 'A3'
                    }
                }
            }
        }
        cls.config_path = path.join(path.dirname(path.realpath(__file__)), 'test_runtime.json')
        cls.cache = URICache(data=cls.defaults)

    @classmethod
    def tearDownClass(cls):
        cls.config_path = path.join(path.dirname(path.realpath(__file__)), 'test_runtime.json')
        remove(cls.config_path)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_cache(self):
        cache = URICache()
        self.assertEqual(cache.get(), {})

        self.assertEqual(self.cache.get(), self.defaults)
        self.cache.save(self.config_path)

        cache = URICache(self.config_path)
        self.assertEqual(cache.get(), self.defaults)

    def test_set(self):
        self.cache.set(True, 'level1/level2/level3/target')
        self.assertEqual(self.cache.get('level1/level2/level3/target'), True)

    def test_get(self):
        self.assertEqual(self.cache.get('level1/a1'), 'A1')
        self.assertEqual(self.cache.get('level1/level2/level3'), {'a3': 'A3'})

    def test_load(self):
        defaults = {
            'level1': {
                'a1': 'A1',
                'level2': {
                    'a2': 'A2',
                    'level3': {
                        'a3': 'A3'
                    }
                }
            }
        }
        loaded_data = self.cache.load(self.config_path)
        self.assertEqual(loaded_data, defaults)

    def test_save(self):
        defaults = self.cache.get()
        self.cache.save(self.config_path)
        self.assertEqual(defaults, self.cache.load(self.config_path))

    def test_update(self):
        data = {'value1': 1, 'value2': {'value3': 3, 'value4': 4}}

        self.cache.update(data, 'level1/level2/level3')
        self.assertEqual(self.cache.get('level1/level2/level3/value1'), 1)
        self.assertEqual(self.cache.get('level1/level2/level3/value2'), data.get('value2'))

        self.cache.update({'AA': 'B123'}, 'level1/level2/level3/a3')
        self.assertEqual(self.cache.get('level1/level2/level3/a3'), {'AA': 'B123'})

        self.cache.update('test', 'level1/a1')
        self.assertEqual('test', self.cache.get('level1/a1'))

    def test_remove(self):
        defaults = {
            'level1': {
                'a1': 'A1',
                'level2': {
                    'a2': 'A2',
                    'level3': {}
                }
            }
        }
        self.cache.remove('level1/level2/level3/a3')
        self.assertEqual(defaults, self.cache.get())

        defaults = {'level1': {'a1': 'A1'}}
        self.cache.remove('level1/level2')
        self.assertEqual(defaults, self.cache.get())

    def test_sanitize_uri(self):
        uri = 'level1\level2\level3\\a123'
        self.assertEqual(self.cache.sanitize(uri), 'level1/level2/level3/a123')


if __name__ == '__main__':
    main()
