#!/usr/bin/env python
# coding: utf-8

import os
import unittest

from mkdocs import nav, utils


class UtilsTests(unittest.TestCase):
    def test_html_path(self):
        expected_results = {
            'index.md': 'index.html',
            'api-guide.md': 'api-guide/index.html',
            'api-guide/index.md': 'api-guide/index.html',
            'api-guide/testing.md': 'api-guide/testing/index.html',
        }
        for file_path, expected_html_path in expected_results.items():
            html_path = utils.get_html_path(file_path)
            self.assertEqual(html_path, expected_html_path)

    def test_url_path(self):
        expected_results = {
            'index.md': '/',
            'api-guide.md': '/api-guide/',
            'api-guide/index.md': '/api-guide/',
            'api-guide/testing.md': '/api-guide/testing/',
        }
        for file_path, expected_html_path in expected_results.items():
            html_path = utils.get_url_path(file_path)
            self.assertEqual(html_path, expected_html_path)

    def test_is_markdown_file(self):
        expected_results = {
            'index.md': True,
            'index.MARKDOWN': True,
            'index.txt': False,
            'indexmd': False
        }
        for path, expected_result in expected_results.items():
            is_markdown = utils.is_markdown_file(path)
            self.assertEqual(is_markdown, expected_result)

    def test_is_html_file(self):
        expected_results = {
            'index.htm': True,
            'index.HTML': True,
            'index.txt': False,
            'indexhtml': False
        }
        for path, expected_result in expected_results.items():
            is_html = utils.is_html_file(path)
            self.assertEqual(is_html, expected_result)

    def test_create_media_urls(self):
        pages = [
            {'Home': 'index.md'},
            {'About': 'about.md'},
            {'Sub': [
                {'Sub Home': 'index.md'},
                {'Sub About': 'about.md'},

            ]}
        ]
        expected_results = {
            'https://media.cdn.org/jq.js': 'https://media.cdn.org/jq.js',
            'http://media.cdn.org/jquery.js': 'http://media.cdn.org/jquery.js',
            '//media.cdn.org/jquery.js': '//media.cdn.org/jquery.js',
            'media.cdn.org/jquery.js': './media.cdn.org/jquery.js',
            'local/file/jquery.js': './local/file/jquery.js',
            'image.png': './image.png',
        }
        site_navigation = nav.SiteNavigation(pages)
        for path, expected_result in expected_results.items():
            urls = utils.create_media_urls(site_navigation, [path])
            self.assertEqual(urls[0], expected_result)

    def test_create_relative_media_url_sub_index(self):
        '''
        test special case where there's a sub/index.md page
        '''

        site_navigation = nav.SiteNavigation([
            {'Home': 'index.md'},
            {'Sub': [
                {'Sub Home': '/subpage/index.md'},

            ]}
        ])
        site_navigation.url_context.set_current_url('/subpage/')
        site_navigation.file_context.current_file = "subpage/index.md"

        def assertPathGenerated(declared, expected):
            url = utils.create_relative_media_url(site_navigation, declared)
            self.assertEqual(url, expected)

        assertPathGenerated("img.png", "./img.png")
        assertPathGenerated("./img.png", "./img.png")
        assertPathGenerated("/img.png", "../img.png")

    def test_reduce_list(self):
        self.assertEqual(
            utils.reduce_list([1, 2, 3, 4, 5, 5, 2, 4, 6, 7, 8]),
            [1, 2, 3, 4, 5, 6, 7, 8]
        )

    def test_get_themes(self):

        self.assertEqual(
            sorted(utils.get_theme_names()),
            sorted(['flatly', 'cerulean', 'slate', 'bootstrap', 'yeti',
                    'spacelab', 'united', 'readable', 'simplex', 'mkdocs',
                    'cosmo', 'journal', 'cyborg', 'readthedocs', 'amelia']))

    def test_nest_paths(self):

        j = os.path.join

        result = utils.nest_paths([
            'index.md',
            j('user-guide', 'configuration.md'),
            j('user-guide', 'styling-your-docs.md'),
            j('user-guide', 'writing-your-docs.md'),
            j('about', 'contributing.md'),
            j('about', 'license.md'),
            j('about', 'release-notes.md'),
        ])

        self.assertEqual(
            result,
            [
                'index.md',
                {'User guide': [
                    j('user-guide', 'configuration.md'),
                    j('user-guide', 'styling-your-docs.md'),
                    j('user-guide', 'writing-your-docs.md')]},
                {'About': [
                    j('about', 'contributing.md'),
                    j('about', 'license.md'),
                    j('about', 'release-notes.md')]}
            ]
        )
