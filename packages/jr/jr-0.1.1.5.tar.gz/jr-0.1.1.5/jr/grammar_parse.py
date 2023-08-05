from textx import metamodel_from_str


class GrammarParse(object):
    def __init__(self, lang_tx_str):
        self._lang_tx_str = lang_tx_str
        self.grammar_model = None

    def parse(self, dsl_str):
        tree_meta = metamodel_from_str(self._lang_tx_str)
        self.grammar_model = tree_meta.model_from_str(dsl_str, debug=False)
        return self.grammar_model
