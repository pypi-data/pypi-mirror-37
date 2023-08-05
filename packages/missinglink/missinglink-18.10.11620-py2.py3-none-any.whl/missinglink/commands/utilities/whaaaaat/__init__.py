# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import os
from .prompt import prompt
from .separator import Separator
from .prompts.common import default_style

__version__ = '0.5.2'


def here(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class PromptParameterException(ValueError):
    def __init__(self, message, errors=None):

        # Call the base class constructor with the parameters it needs
        super(PromptParameterException, self).__init__(
            'You must provide a `%s` value' % message, errors)
