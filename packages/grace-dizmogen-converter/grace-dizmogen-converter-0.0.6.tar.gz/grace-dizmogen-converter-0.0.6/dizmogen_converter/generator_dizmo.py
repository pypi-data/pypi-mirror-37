import os
import tempfile
import subprocess
import shlex
import json
import re
import shutil
from bs4 import Comment
from dizmogen_converter.exceptions import GeneratorDizmoError


class GeneratorDizmo(object):
    def __init__(self, config):
        self._name = ''

        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', config['name'])
        for m in matches:
            self._name += m.group(0).lower() + '-'
        self._name = self._name[:-1]

        # self._name = config['name']
        self._bundleid = config['bundleid']
        self._coffeescript = config['coffeescript']

        if config['author'] is not None:
            self._author = config['author']
        else:
            self._author = 'Grace DizmoGen Converter'

        if config['email'] is not None:
            self._email = config['email']
        else:
            self._email = 'support@dizmo.com'

        if config['description'] is not None:
            self._description = config['description']
        else:
            self._description = 'Converted using the python module dizmogen_converter.'

        self._cwd = os.getcwd()
        self._tempdir = tempfile.mkdtemp()

    def load(self):
        os.chdir(self._tempdir)

        args = 'yo @dizmo/dizmo "{}" --bundle-id {} --description "{}" --author "{}" --email "{}"'.format(self._name, self._bundleid, self._description, self._author, self._email)

        if self._coffeescript:
            args += ' --coffeescript'

        args = shlex.split(args)
        proc = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.chdir(self._cwd)
        if proc.returncode != 0:
            raise GeneratorDizmoError('Could not create the new dizmo skeleton through the generator-dizmo node module.')

        self._load_config()

    def _load_config(self):
        with open(os.path.join(self._tempdir, self._name.lower(), 'package.json')) as f:
            self._config = json.load(f)

        self._config['dizmo']['build']['minify'] = {}

    def write_config_diff(self, updates):
        self._config = self._update_config(self._config, updates)

        if len(self._config['version'].split('.')) < 3:
            self._config['version'] = self._config['version'] + '.0'

        config_file_path = os.path.join(self._tempdir, self._name.lower(), 'package.json')

        if os.path.exists(config_file_path):
            os.remove(config_file_path)

        with open(config_file_path, 'a+') as f:
            json.dump(self._config, f, indent=2)
            f.write('\n')

    def _update_config(self, config, updates):
        for key, value in updates.items():
            if key not in config or not isinstance(value, dict):
                config[key] = value
            else:
                config[key] = self._update_config(config[key], value)

        return config

    def write_html(self, html_soup):
        script_tags = []
        for tag in html_soup.head.find_all('script'):
            script_tags.append(tag.extract())

        html_soup.body.find('script').decompose()
        for tag in script_tags:
            html_soup.body.append(tag)

        index_js = html_soup.new_tag('script', src='index.js')
        html_soup.body.append(index_js)

        for element in html_soup.head(text=lambda text: isinstance(text, Comment)):
            element.extract()

        html_file_path = os.path.join(self._tempdir, self._name.lower(), 'src', 'index.html')

        if os.path.exists(html_file_path):
            os.remove(html_file_path)

        with open(html_file_path, 'a+') as f:
            f.write(html_soup.prettify())
            f.write('\n')

    def write_plain_js(self, js_string):
        js_file_path = os.path.join(self._tempdir, self._name.lower(), 'src', 'index.js')

        if os.path.exists(js_file_path):
            os.remove(js_file_path)

        with open(js_file_path, 'a+') as f:
            f.write(js_string)
            f.write('\n')

    def copy_libs(self):
        gen_lib_dir = os.path.join(self._tempdir, self._name.lower(), 'src', 'lib')
        grace_lib_dir = os.path.join(self._cwd, 'src', 'lib')

        i18n_fp = os.path.join(gen_lib_dir, 'i18n-1.0.6.min.js')
        shutil.copy(i18n_fp, os.path.join(self._tempdir, 'i18n'))
        shutil.rmtree(gen_lib_dir)

        shutil.copytree(grace_lib_dir, gen_lib_dir)
        shutil.copy(os.path.join(self._tempdir, 'i18n'), os.path.join(gen_lib_dir, 'i18n-1.0.6.min.js'))

        os.remove(os.path.join(self._tempdir, 'i18n'))

    def copy_styles(self):
        gen_style_dir = os.path.join(self._tempdir, self._name.lower(), 'src', 'style')
        grace_style_dir = os.path.join(self._cwd, 'src', 'style')

        shutil.rmtree(gen_style_dir)
        shutil.copytree(grace_style_dir, gen_style_dir)

    def copy_assets(self):
        gen_assets_dir = os.path.join(self._tempdir, self._name.lower(), 'assets')
        grace_assets_dir = os.path.join(self._cwd, 'assets')

        locales_dir = os.path.join(gen_assets_dir, 'locales')
        shutil.copytree(locales_dir, os.path.join(self._tempdir, 'locales'))

        shutil.rmtree(gen_assets_dir)
        shutil.copytree(grace_assets_dir, gen_assets_dir)
        shutil.copytree(os.path.join(self._tempdir, 'locales'), os.path.join(gen_assets_dir, 'locales'))
        shutil.rmtree(os.path.join(self._tempdir, 'locales'))

    def copy_coffeescript(self):
        self._copy_coffeescript('application', os.path.join(self._cwd, 'src'), os.path.join(self._tempdir, self._name.lower(), 'src'), [])

        index_coffee = os.path.join(self._tempdir, self._name.lower(), 'src', 'index.coffee')
        application_coffee = os.path.join(self._tempdir, self._name.lower(), 'src', 'application.coffee')

        os.remove(index_coffee)
        shutil.copy(application_coffee, index_coffee)
        os.remove(application_coffee)

    def _copy_coffeescript(self, filename, old_path, new_path, required):
        file_content = ''

        with open(os.path.join(old_path, filename + '.coffee')) as f:
            line = f.readline()
            while line:
                if line.strip().startswith('#= require'):
                    if line.strip() not in required:
                        required.append(line.strip())

                        subpath = line.strip()[11:].split('/')
                        op = os.path.join(self._cwd, 'src', 'javascript', os.sep.join(subpath[:-1]))
                        np = os.path.join(self._tempdir, self._name.lower(), 'src', 'js', os.sep.join(subpath[:-1]))
                        fn = subpath[-1]

                        self._copy_coffeescript(fn, op, np, required)
                        if filename == 'application':
                            line = "require './js/" + line.strip()[11:] + ".coffee'\n"
                        else:
                            line = "require './" + line.strip()[11:] + ".coffee'\n"
                    else:
                        line = ''

                file_content += line
                line = f.readline()

        os.makedirs(new_path, exist_ok=True)
        with open(os.path.join(new_path, filename + '.coffee'), 'a+') as f:
            f.write(file_content)
            f.write('\n')

    def copy_source(self):
        new_name = os.path.basename(self._cwd) + '__converted'
        new_path = os.path.join(os.sep.join(self._cwd.split('/')[:-1]), new_name)

        if os.path.exists(new_path):
            shutil.rmtree(new_path)

        shutil.copytree(os.path.join(self._tempdir, self._name.lower()), new_path)

        print('The converted dizmo can be found at ' + new_path + '. You can now run "npm install" in that directory to set up dizmo-generator.')

    def remove_tempdir(self):
        shutil.rmtree(self._tempdir)
