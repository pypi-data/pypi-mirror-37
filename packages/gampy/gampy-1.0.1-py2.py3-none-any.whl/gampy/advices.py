#!/usr/bin/env python
# coding: utf-8

# In[8]:


"""Advices of the project."""

import logging

from typing import Any, Type, Callable

from functools import wraps, lru_cache

from gampy.structures import Advice


# In[ ]:


def identical() -> Advice:
    """Return f as is."""

    def advice(f):
        return f

    return advice


# In[16]:


def cacheable(n: int = 128, typed: bool = False) -> Advice:
    """Cache the n most recent results."""
    return lru_cache(n, typed)


# In[3]:


def constable(x: Any = None) -> Advice:
    """Return x constantly."""

    def advice(f):
        @wraps(f)
        def wrapped(*_, **__):
            return x

        return wrapped

    return advice


# In[2]:


def flippable() -> Advice:
    """Flip f arguments."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*reversed(args), **kwargs)

        return wrapped

    return advice


# In[4]:


def fluentable(n: int = 0) -> Advice:
    """Return the nth argument of f."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            state = f(*args, **kwargs)

            try:
                return args[n]
            except IndexError:
                return state

        return wrapped

    return advice


# In[ ]:


def preable(do: Callable[[], None]) -> Advice:
    """Call do before f."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            do()

            return f(*args, **kwargs)

        return wrapped

    return advice


# In[6]:


def postable(do: Callable[[], None]) -> Advice:
    """Call do after f."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            state = f(*args, **kwargs)
            do()

            return state

        return wrapped

    return advice


# In[2]:


def optional(x: Any) -> Advice:
    """Return x when f returns None."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            state = f(*args, **kwargs)

            if state is None:
                return x

            return state

        return wrapped

    return advice


# In[ ]:


def retryable(d: Any = None, n: int = 3, on: Type[Exception] = Exception) -> Advice:
    """Retry f n times until success."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for _ in range(n):
                try:
                    return f(*args, **kwargs)
                except on:
                    pass

            return d

        return wrapped

    return advice


# In[5]:


def exceptional(x: Any = None, on: Type[Exception] = Exception) -> Advice:
    """Return x when f raises an exception."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except on:
                return x

        return wrapped

    return advice


# In[4]:


def loggable(
    logger: Callable[[str], None] = logging.info, pre: bool = True, post: bool = True
) -> Advice:
    """Log f before and/or after call."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if pre:
                logger("enter: {}".format(f.__name__))

            state = f(*args, **kwargs)

            if post:
                logger("exit: {}".format(f.__name__))

            return state

        return wrapped

    return advice


# In[7]:


def traceable(
    printer: Callable[[str], None] = print, pre: bool = True, post: bool = False
) -> Advice:
    """Print f trace before and/or after call."""

    def advice(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            strf = f.__name__
            strargs = [str(x) for x in args]
            strkwargs = ["{0}={1}".format(k, v) for k, v in kwargs.items()]
            inittrace = "{0}({1})".format(strf, ",".join(strargs + strkwargs))

            if pre:
                printer("[PRE] {}".format(inittrace))

            state = f(*args, **kwargs)
            exittrace = str(state)

            if post:
                printer("[POST] {} -> {}".format(inittrace, exittrace))

            return state

        return wrapped

    return advice
