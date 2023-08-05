# -*- coding: utf-8 -*-
from .extension import Extension
from .grammar_parse import GrammarParse
from .render import Render


class Parser(object):
    def __init__(self, dsl_str, lang_tx_str, template_path, extension=Extension(), grammar_parse=None, render=None):
        self._dsl_str = dsl_str
        self._lang_tx_str = lang_tx_str
        self._template_path = template_path
        self._extension = extension
        self._grammar_parse = self._get_grammar_parse(grammar_parse)
        self._render = self._get_render(render)
        self.out_code = ''

    def parse(self):
        # DSL 预处理
        self._dsl_str = self._extension.preprocess(self._dsl_str)
        # 语法分析
        grammar_model = self._grammar_parse.parse(self._dsl_str)
        # 语义分析
        grammar_model = self._extension.semantic_parse(grammar_model)
        # 代码生成
        self.out_code = self._render.run(grammar_model)
        # 代码优化
        self.out_code = self._extension.code_optimize(self.out_code)
        return self.out_code

    def save_to(self, file_name):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.out_code)

    def save(self, file_name):
        self.save_to(file_name)

    def _get_grammar_parse(self, grammar_parse):
        if grammar_parse is None:
            grammar_parse = GrammarParse(self._lang_tx_str)
        return grammar_parse

    def _get_render(self, render):
        if render is None:
            render = Render(self._template_path)
        return render
