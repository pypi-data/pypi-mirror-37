'''Test the ability to add a label to a (potentially trained) parsing model.'''
from __future__ import unicode_literals
import pytest
import numpy.random

from ...attrs import NORM
from ...gold import GoldParse
from ...vocab import Vocab
from ...tokens import Doc
from ...pipeline import LinearDependencyParser as DependencyParser

numpy.random.seed(0)



def test_init_parser():
    parser = DependencyParser(Vocab())

def test_init_parser_model():
    parser = DependencyParser(Vocab())
    parser.begin_training([])
    assert parser.moves.labels


def test_call_parser():
    parser = DependencyParser(Vocab())
    parser.begin_training([])
    doc = Doc(parser.vocab, words=['a', 'b', 'c', 'd'])
    parser(doc)
