"""
encoding package

This package provides utilities for encoding and decoding text, including a metaclass for ensuring method implementations,
a pipeline for sequential encoding steps, and functionality for adding and removing random characters (salt) from text.

Modules:
    utils: Provides TextEncoder, Pipeline, and Salt for text encoding and transformation.
"""

from .utils import TextEncoder, Pipeline, Salt

__all__ = [
    'TextEncoder',
    'Pipeline',
    'Salt'
]
