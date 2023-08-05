# coding: utf8
from __future__ import unicode_literals

from ...attrs import LANG
from ...language import Language
from ...tokens import Doc


class ChineseDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda text: 'zh'  # for pickling


class Chinese(Language):
    lang = 'zh'
    Defaults = ChineseDefaults  # override defaults

    def make_doc(self, text):
        words = []
        spaces = []
        doc = self.tokenizer(text)
        for token in self.tokenizer(text):
            words.extend(list(token.text))
            spaces.extend([False]*len(token.text))
            spaces[-1] = bool(token.whitespace_)
        return Doc(self.vocab, words=words, spaces=spaces)


__all__ = ['Chinese']
