#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""Errors of the project."""


class Error(Exception):
    """Base class for errors."""

    pass


class DefinitionError(Error):
    """Error during definition."""

    pass


class CompositionError(Error):
    """Error during composition."""

    pass
