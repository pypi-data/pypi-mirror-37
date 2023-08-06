
import os
import re
from importlib import import_module
from .genuslist import genus_list

def obtain_genus(rulestring):

    for g in genus_list:
        m = re.match(g['regex'] + '$', rulestring)
        if m is not None:
            return g['name']

    raise ValueError('Rule "%s" does not belong to any genus' % rulestring)

def genus_to_module(genus):

    m = import_module('.' + genus, __name__)

    return m

def rule_property(rulestring, attribute):

    m = genus_to_module(obtain_genus(rulestring))
    attr = getattr(m, attribute)
    if callable(attr):
        attr = attr(rulestring)
    return attr

def create_rule(rulestring):

    rule_property(rulestring, 'create_rule')
