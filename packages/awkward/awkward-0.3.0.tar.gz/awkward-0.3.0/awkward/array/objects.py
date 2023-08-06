#!/usr/bin/env python

# Copyright (c) 2018, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import importlib
import pickle

import awkward.array.base
import awkward.type
import awkward.util

class Methods(object):
    @staticmethod
    def mixin(methods, awkwardtype):
        assert issubclass(methods, Methods)
        assert not issubclass(methods, awkward.array.base.AwkwardArray)
        assert issubclass(awkwardtype, awkward.array.base.AwkwardArray)
        assert not issubclass(awkwardtype, Methods)
        return type(awkwardtype.__name__ + "Methods", (methods, awkwardtype), {})

    @staticmethod
    def maybemixin(sample, awkwardtype):
        if issubclass(sample, Methods):
            assert issubclass(sample, awkward.array.base.AwkwardArray)
            assert issubclass(awkwardtype, awkward.array.base.AwkwardArray)
            allbases = tuple(x for x in sample.__bases__ if not issubclass(x, awkward.array.base.AwkwardArray)) + (awkwardtype,)
            return type(awkwardtype.__name__ + "Methods", allbases, {})
        else:
            return awkwardtype

class ObjectArray(awkward.array.base.AwkwardArrayWithContent):
    def __init__(self, content, generator, *args, **kwargs):
        self.content = content
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def copy(self, content=None, generator=None, args=None, kwargs=None):
        out = self.__class__.__new__(self.__class__)
        out._content = self._content
        out._generator = self._generator
        out._args = self._args
        out._kwargs = self._kwargs
        if content is not None:
            out.content = content
        if generator is not None:
            out.generator = generator
        if args is not None:
            out.args = args
        if kwargs is not None:
            out.kwargs = kwargs
        return out

    def deepcopy(self, content=None, generator=None, args=None, kwargs=None):
        out = self.copy(content=content, generator=generator, args=args, kwargs=kwargs)
        out._content = awkward.util.deepcopy(out._content)
        return out

    def empty_like(self, **overrides):
        mine = {}
        mine["generator"] = overrides.pop("generator", self._generator)
        mine["args"] = overrides.pop("args", self._args)
        mine["kwargs"] = overrides.pop("kwargs", self._kwargs)
        if isinstance(self._content, awkward.util.numpy.ndarray):
            return self.copy(content=awkward.util.numpy.empty_like(self._content), **mine)
        else:
            return self.copy(content=self._content.empty_like(**overrides), **mine)

    def zeros_like(self, **overrides):
        mine = {}
        mine["generator"] = overrides.pop("generator", self._generator)
        mine["args"] = overrides.pop("args", self._args)
        mine["kwargs"] = overrides.pop("kwargs", self._kwargs)
        if isinstance(self._content, awkward.util.numpy.ndarray):
            return self.copy(content=awkward.util.numpy.zeros_like(self._content), **mine)
        else:
            return self.copy(content=self._content.zeros_like(**overrides), **mine)

    def ones_like(self, **overrides):
        mine = {}
        mine["generator"] = overrides.pop("generator", self._generator)
        mine["args"] = overrides.pop("args", self._args)
        mine["kwargs"] = overrides.pop("kwargs", self._kwargs)
        if isinstance(self._content, awkward.util.numpy.ndarray):
            return self.copy(content=awkward.util.numpy.ones_like(self._content), **mine)
        else:
            return self.copy(content=self._content.ones_like(**overrides), **mine)

    def __awkward_persist__(self, ident, fill, **kwargs):
        self._valid()

        if self._generator.__module__ == "__main__":
            raise TypeError("cannot persist ObjectArray: its generator is defined in __main__, which won't be available in a subsequent session")
        if hasattr(self._generator, "__qualname__"):
            spec = [self._generator.__module__] + self._generator.__qualname__.split(".")
        else:
            spec = [self._generator.__module__, self._generator.__name__]

        gen, genname = importlib.import_module(spec[0]), spec[1:]
        while len(genname) > 0:
            gen, genname = getattr(gen, genname[0]), genname[1:]
        if gen is not self._generator:
            raise TypeError("cannot persist ObjectArray: its generator cannot be found via its __name__ (Python 2) or __qualname__ (Python 3)")

        n = self.__class__.__name__
        out = {"id": ident,
               "call": ["awkward", n],
               "args": [fill(self._content, n + ".content", **kwargs), {"function": spec}]}
        if len(self._args) > 0:
            out["*"] = {"call": ["pickle", "loads"], "args": [pickle.dumps(self._args)]}
        if len(self._kwargs) > 0:
            out["**"] = {"call": ["pickle", "loads"], "args": [pickle.dumps(self._kwargs)]}

        return out

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = awkward.util.toarray(value, awkward.util.DEFAULTTYPE)

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, value):
        if not callable(value):
            raise TypeError("generator must be a callable (of one argument: the array slice)")
        self._generator = value

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if not isinstance(value, tuple):
            value = (value,)
        self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if not isinstance(value, dict):
            raise TypeError("kwargs must be a dict")
        self._kwargs = value

    def __len__(self):
        return len(self._content)

    def _gettype(self, seen):
        if len(self._content.shape) == 1:
            return self._generator
        else:
            return awkward.type.ArrayType(*(self._content.shape[1:] + (self._generator,)))

    def _getshape(self):
        return (len(self._content),)

    def _valid(self):
        pass
        
    def __iter__(self):
        for x in self._content:
            yield self.generator(x, *self._args, **self._kwargs)

    def __getitem__(self, where):
        if awkward.util.isstringslice(where):
            return self._content[where]

        if isinstance(where, tuple) and where == ():
            return self
        if not isinstance(where, tuple):
            where = (where,)
        head, tail = where[0], where[1:]

        content = self._content[head]
        if isinstance(head, awkward.util.integer):
            if isinstance(tail, tuple) and tail == ():
                return self.generator(content, *self._args, **self._kwargs)
            else:
                return self.generator(content, *self._args, **self._kwargs)[tail]

        elif isinstance(tail, tuple) and tail == ():
            return self.copy(content=content)

        else:
            return [x[tail] for x in content]

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method != "__call__":
            return NotImplemented

        contents = []
        for x in inputs:
            if isinstance(x, ObjectArray):
                x._valid()
                contents.append(x._content)
            else:
                contents.append(x)

        result = getattr(ufunc, method)(*contents, **kwargs)

        if awkward.util.iscomparison(ufunc):
            return result
        else:
            return self.copy(content=result)

    def any(self):
        return any(x for x in self)

    def all(self):
        return all(x for x in self)

    @classmethod
    def concat(cls, first, *rest):
        raise NotImplementedError

    def pandas(self):
        raise NotImplementedError
