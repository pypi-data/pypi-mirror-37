import itertools


class MultiQuerySet(object):

    def __init__(self, querysets):
        self.querysets = list(querysets)

    def __iter__(self):
        return itertools.chain.from_iterable(self.querysets)

    def iterator(self):
        return itertools.chain.from_iterable(x.iterator() for x in self.querysets)

    def count(self):
        return sum(x.count() for x in self.querysets)

    def values(self, *fields, **expressions):
        return self.__class__(q.values(*fields, **expressions) for q in self.querysets)

    def values_list(self, *fields, flat=False, named=False):
        return self.__class__(q.values_list(*fields, flat=flat, named=named) for q in self.querysets)

    def first_or_default(self, default=None):
        return next(iter(self), default)


def step_query(bulk, callable, step=1000):
    bulk = list(bulk)
    querysets = []
    for _, bucket in itertools.groupby(enumerate(bulk), lambda k: int(k[0]/step)):
        batch = list(x[1] for x in bucket)
        querysets.append(callable(batch))
    return MultiQuerySet(querysets)

