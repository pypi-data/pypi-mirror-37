from itertools import chain


class Attrs:
    "Helper class to be able to access values using ."
    def __init__(self, key, val):
        self.__dict__[key] = val


class Word:
    "A single word. We store what's needed as of now."
    __slots__ = ['text', 'i', 'idx', 'pos_', 'ent_type_',
                 'tag_', 'dep_', 'cluster', 'dunder_attrs',
                 'sent_start_idx']

    def __init__(self, w):
        self.text = w.text
        self.i = w.i
        self.idx = w.idx
        self.pos_ = w.pos_
        self.ent_type_ = w.ent_type_
        self.tag_ = w.tag_
        self.dep_ = w.dep_
        self.cluster = w.cluster
        self.sent_start_idx = w.sent[0].i

        try:
            clusters = [Attrs('i', cl.i) for cl in w._.coref_clusters]
        except TypeError:
            self.dunder_attrs = None
        else:
            self.dunder_attrs = Attrs('coref_clusters', clusters)

    @property
    def _(self):  # The coref attrs
        if self.dunder_attrs is None:
            raise TypeError('Original did not have iterable coref_clusters')
        return self.dunder_attrs

    def __repr__(self):
        return self.text
    
    def __str__(self):
        return self.text


class Doc:
    __slots__ = ['words']

    def __init__(self, doc):
        self.words = [Word(w) for w in doc]

    def __len__(self):
        return sum([len(s) for s in self.sents])

    def __iter__(self):
        for i in chain(*self.sents):
            yield i

    def __getitem__(self, *args):
        return self.words.__getitem__(*args)

    def char_span(self, s, e):
        found = False
        span = []
        for i, w in enumerate(self.words):
            if w.idx >= e:
                found = True
                break
            if w.idx >= s:
                span.append(w)
        if not found:
            return None
        return span

    @property
    def sents(self):
        span, last_sent_idx = [], None
        for w in self.words:
            if last_sent_idx is not None:
                if last_sent_idx != w.sent_start_idx:
                    # sentence has changed
                    yield span
                    span = []
            last_sent_idx = w.sent_start_idx
            span.append(w)
        if len(span) != 0:
            yield span
