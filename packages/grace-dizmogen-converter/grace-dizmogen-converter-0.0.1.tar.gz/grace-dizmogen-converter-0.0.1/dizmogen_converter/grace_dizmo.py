import os
import re
import json
from bs4 import BeautifulSoup


class GraceDizmo(object):
    def __init__(self):
        self._cwd = os.getcwd()
        self._config = self._gather_info()
        self._coffeescript = False
        self._html_soup = self._load_html()

        for fname in os.listdir(os.path.join(self._cwd, 'src', 'javascript')):
            if fname.endswith('.coffee'):
                self._coffeescript = True

    def _gather_info(self):
        config_file = os.path.join(self._cwd, 'project.cfg')
        return self._parse_cfg_file(open(config_file))

    def _parse_cfg_file(self, config_file):
        strings = []
        for line in config_file:
            if not re.search('^\s*//.*', line):
                strings.append(line.strip())

        return json.loads(''.join(strings))

    def _load_html(self):
        html_file = os.path.join(self._cwd, 'src', 'index.html')
        with open(html_file, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        return soup

    def get_plain_js(self):
        if self._coffeescript:
            return None

        main_js = os.path.join(self._cwd, 'src', 'application.js')
        return self._gather_js(main_js, '', [])

    def _gather_js(self, js_file_path, js_string, included):
        with open(js_file_path, 'r') as f:
            line = f.readline()
            while line:
                if line.strip().startswith('//= require'):
                    if line.strip() not in included:
                        included.append(line.strip())
                        include_path = os.path.join(self._cwd, 'src', 'javascript', line.strip()[12:] + '.js')
                        js_string += self._gather_js(include_path, js_string, included)
                else:
                    js_string += line

                line = f.readline()

        return js_string

    def get_html(self):
        return self._html_soup

    def get_generator_info(self):
        config = {
            'name': self._config['name'],
            'bundleid': self._config['dizmo_settings']['bundle_identifier'],
            'author': None,
            'email': None,
            'description': None,
            'coffeescript': self._coffeescript
        }

        if 'author' in self._config:
            config['author'] = self._config['author']
        if 'author' in self._config['dizmo_settings']:
            config['author'] = self._config['dizmo_settings']['author']

        if 'email' in self._config:
            config['email'] = self._config['email']
        if 'email' in self._config['dizmo_settings']:
            config['email'] = self._config['dizmo_settings']['email']

        if 'description' in self._config['dizmo_settings']:
            config['description'] = self._config['dizmo_settings']['description']

        return config

    def get_config_diff(self):
        diff = {
            'version': self._config['version'],
            'dizmo': {
                'settings': {
                    'category': self._config['dizmo_settings']['category'],
                    'tags': self._config['dizmo_settings']['tags'],
                    'height': self._config['dizmo_settings']['height'],
                    'width': self._config['dizmo_settings']['width'],
                    'bundle-name': self._config['dizmo_settings']['bundle_name'],
                    'display-name': self._config['dizmo_settings']['display_name'],
                    'elements-version': self._config['dizmo_settings']['elements_version'],
                    'api-version': self._config['dizmo_settings']['api_version'],
                    'change-log': self._config['dizmo_settings']['change_log'],
                    'attributes': {}
                },
                'build': {
                    'minify': {
                        'markup': False,
                        'scripts': False,
                        'styles': False
                    },
                },
                'store': {}
            }
        }

        if 'tree_values' in self._config['dizmo_settings'] and 'attributes' in self._config['dizmo_settings']['tree_values']:
            for key, value in self._config['dizmo_settings']['tree_values']['attributes']:
                diff['dizmo']['settings']['attributes'][key] = value

        if 'urls' in self._config['dizmo_settings'] and 'dizmo_store' in self._config['dizmo_settings']['urls']:
            diff['dizmo']['store']['host'] = self._config['dizmo_settings']['urls']['dizmo_store'][:-3]

        if 'minify_js' in self._config:
            diff['dizmo']['build']['minify']['scripts'] = self._config['minify_js']

        if 'minify_css' in self._config:
            diff['dizmo']['build']['minify']['styles'] = self._config['minify_css']

        return diff
