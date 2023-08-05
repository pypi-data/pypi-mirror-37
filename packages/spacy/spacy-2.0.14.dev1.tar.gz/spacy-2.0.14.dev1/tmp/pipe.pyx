from __future__ import unicode_literals
import cytoolz
from collections import OrderedDict, defaultdict
import ujson
import numpy
cimport numpy as np

from . import util
from ._ml import link_vectors_to_models, zero_init, flatten
from ._ml import create_default_optimizer
from .compat import json_dumps

class Pipe(object):
    """This class is not instantiated directly. Components inherit from it, and
    it defines the interface that components should follow to function as
    components in a spaCy analysis pipeline.
    """
    name = None

    @classmethod
    def Model(cls, *shape, **kwargs):
        """Initialize a model for the pipe."""
        raise NotImplementedError

    def __init__(self, vocab, model=True, **cfg):
        """Create a new pipe instance."""
        raise NotImplementedError

    def __call__(self, doc):
        """Apply the pipe to one document. The document is
        modified in-place, and returned.

        Both __call__ and pipe should delegate to the `predict()`
        and `set_annotations()` methods.
        """
        scores, tensors = self.predict([doc])
        self.set_annotations([doc], scores, tensors=tensors)
        return doc

    def pipe(self, stream, batch_size=128, n_threads=-1):
        """Apply the pipe to a stream of documents.

        Both __call__ and pipe should delegate to the `predict()`
        and `set_annotations()` methods.
        """
        for docs in cytoolz.partition_all(batch_size, stream):
            docs = list(docs)
            scores, tensors = self.predict(docs)
            self.set_annotations(docs, scores, tensor=tensors)
            yield from docs

    def predict(self, docs):
        """Apply the pipeline's model to a batch of docs, without
        modifying them.
        """
        raise NotImplementedError

    def set_annotations(self, docs, scores, tensors=None):
        """Modify a batch of documents, using pre-computed scores."""
        raise NotImplementedError

    def update(self, docs, golds, drop=0., sgd=None, losses=None):
        """Learn from a batch of documents and gold-standard information,
        updating the pipe's model.

        Delegates to predict() and get_loss().
        """
        raise NotImplementedError

    def get_loss(self, docs, golds, scores):
        """Find the loss and gradient of loss for the batch of
        documents and their predicted scores."""
        raise NotImplementedError

    def add_label(self, label):
        """Add an output label, to be predicted by the model.

        It's possible to extend pre-trained models with new labels,
        but care should be taken to avoid the "catastrophic forgetting"
        problem.
        """
        raise NotImplementedError

    def create_optimizer(self):
        return create_default_optimizer(self.model.ops,
                                        **self.cfg.get('optimizer', {}))

    def begin_training(self, get_gold_tuples=lambda: [], pipeline=None, sgd=None,
                       **kwargs):
        """Initialize the pipe for training, using data exampes if available.
        If no model has been initialized yet, the model is added."""
        if self.model is True:
            self.model = self.Model(**self.cfg)
        link_vectors_to_models(self.vocab)
        if sgd is None:
            sgd = self.create_optimizer()
        return sgd

    def use_params(self, params):
        """Modify the pipe's model, to use the given parameter values."""
        with self.model.use_params(params):
            yield

    def to_bytes(self, **exclude):
        """Serialize the pipe to a bytestring."""
        serialize = OrderedDict()
        serialize['cfg'] = lambda: json_dumps(self.cfg)
        if self.model in (True, False, None):
            serialize['model'] = lambda: self.model
        else:
            serialize['model'] = self.model.to_bytes
        serialize['vocab'] = self.vocab.to_bytes
        return util.to_bytes(serialize, exclude)

    def from_bytes(self, bytes_data, **exclude):
        """Load the pipe from a bytestring."""
        def load_model(b):
            # TODO: Remove this once we don't have to handle previous models
            if self.cfg.get('pretrained_dims') and 'pretrained_vectors' not in self.cfg:
                self.cfg['pretrained_vectors'] = self.vocab.vectors.name
            if self.model is True:
                self.model = self.Model(**self.cfg)
            self.model.from_bytes(b)

        deserialize = OrderedDict((
            ('cfg', lambda b: self.cfg.update(ujson.loads(b))),
            ('vocab', lambda b: self.vocab.from_bytes(b)),
            ('model', load_model),
        ))
        util.from_bytes(bytes_data, deserialize, exclude)
        return self

    def to_disk(self, path, **exclude):
        """Serialize the pipe to disk."""
        serialize = OrderedDict()
        serialize['cfg'] = lambda p: p.open('w').write(json_dumps(self.cfg))
        serialize['vocab'] = lambda p: self.vocab.to_disk(p)
        if self.model not in (None, True, False):
            serialize['model'] = lambda p: p.open('wb').write(self.model.to_bytes())
        util.to_disk(path, serialize, exclude)

    def from_disk(self, path, **exclude):
        """Load the pipe from disk."""
        def load_model(p):
            # TODO: Remove this once we don't have to handle previous models
            if self.cfg.get('pretrained_dims') and 'pretrained_vectors' not in self.cfg:
                self.cfg['pretrained_vectors'] = self.vocab.vectors.name
            if self.model is True:
                self.model = self.Model(**self.cfg)
            self.model.from_bytes(p.open('rb').read())

        deserialize = OrderedDict((
            ('cfg', lambda p: self.cfg.update(_load_cfg(p))),
            ('vocab', lambda p: self.vocab.from_disk(p)),
            ('model', load_model),
        ))
        util.from_disk(path, deserialize, exclude)
        return self


def _load_cfg(path):
    if path.exists():
        with path.open() as file_:
            return ujson.load(file_)
    else:
        return {}


