import os
import jinja2
from .filter import *


class Render(object):
    def __init__(self, template_path):
        self._template_path = template_path
        self._template_env = TemplateEnv(template_path)
        self.out_code = ''

    def run(self, grammar_model):
        for node in grammar_model:
            template_file = os.path.join(node.name + '.template')
            if self._template_file_exists(self._template_path, template_file):
                template = self._template_env.load_template(template_file)
                self._gen_code(template, node)
        return self.out_code

    @staticmethod
    def _template_file_exists(template_path, template_file):
        if not os.path.exists(os.path.join(template_path, template_file)):
            raise FileNotFoundError('Error: Can not find template file <%s>' % template_file)
        return True

    def _gen_code(self, template, node):
        self.out_code += template.render(node=node)


class TemplateEnv(object):
    extensions = ['jinja2.ext.do']

    def __init__(self, template_root_path):
        self.__template_root_path = template_root_path
        self.__jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.__template_root_path),
            extensions=self.extensions,
            trim_blocks=True,
            lstrip_blocks=True)
        self.__register_custom_filters()

    def __register_custom_filters(self):
        self.__jinja_env.filters['split_string'] = split_string
        self.__jinja_env.filters['append_list'] = append_list
        self.__jinja_env.filters['trans_list'] = trans_list
        self.__jinja_env.filters['trim_string'] = trim_string
        self.__jinja_env.filters['gen_dict'] = gen_dict
        self.__jinja_env.filters['gen_list'] = gen_list
        self.__jinja_env.filters['trim_comment'] = trim_comment

    def load_template(self, template_file):
        return self.__jinja_env.get_template(template_file)

    def set_template_root_path(self, template_root_path):
        self.__template_root_path = template_root_path

    def get_template_root_path(self):
        return self.__template_root_path
