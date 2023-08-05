# -*- coding: utf-8 -*-
"""
Module utils.py
-----------------
 A set of utility functions that are used to build resources and swagger specification.
"""
import re
import sys
from simple_mappers.object_mapper import JsonObject
from importlib import import_module
import six

# Regex tools used to parse the doc string
PARAM_OR_RETURNS_REGEX = re.compile(r":(?:param|returns|consumes|produces|reaises|version|produces|consumes)")
RETURNS_REGEX = re.compile(r":returns: (?P<doc>.*)", re.S)
PARAM_REGEX = re.compile(
    r":param (?P<name>[\*\w]+): (?P<doc>.*?)"
    r"(?:(?=:param)|(?=:return)|(?=:raises)|(?=:version)|(?=:produces)|(?=:consumes)|\Z)",
    re.S
)
CONSUMES_REGEX = re.compile(
    r":consumes:\s?((\w|/)*)",
    re.S
)
PRODUCES_REGEX = re.compile(
    r":produces:\s?((\w|/)*)",
    re.S
)
VERSION_REGEX = re.compile(
    r":version:\s?((\w|/)*)",
    re.S
)
RAISES_REGEX = re.compile(
    r":raises (?P<name>([\*\w]|\.)+): (?P<doc>.*?)"
    r"(?:(?=:param)|(?=:return)|(?=:raises)|(?=:version)|(?=:produces)|(?=:consumes)|\Z)",
    re.S
)


def trim(docstring):
    """
    trim function from PEP-257
    
    | **function adapted from**
    |    https://github.com/openstack/rally/blob/7153e0cbc5b0e6433313a3bc6051b2c0775d3804/rally/common/plugin/info.py
    
    """
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Current code/unittests expects a line return at
    # end of multiline docstrings
    # workaround expected behavior from unittests
    if "\n" in docstring:
        trimmed.append("")

    # Return a single string:
    return "\n".join(trimmed)


def reindent(string):
    """
    | **function adapted from**
    |    https://github.com/openstack/rally/blob/7153e0cbc5b0e6433313a3bc6051b2c0775d3804/rally/common/plugin/info.py
    
    """
    return "\n".join(l.strip() for l in string.strip().split("\n"))


def parse_docstring(docstring):
    """Parse the docstring into its components.
    
    | **function adapted from**                                                                                        
    | https://github.com/openstack/rally/blob/7153e0cbc5b0e6433313a3bc6051b2c0775d3804/rally/common/plugin/info.py
    
    :returns: a SimpleMappers.JsonObject of form
    
               {
                   "summary": ..., \n
                   "description": ..., \n
                   "params": {"name": "doc"}, \n
                   "returns": ..., \n
                   "consumes":...., \n
                   "produces":....,\n
                   "raises":....., \n
               }
    """

    version = short_description = long_description = returns = ""
    params = {}
    raises = {}
    consumes = []
    produces = []

    if docstring:
        docstring = trim(docstring)

        lines = docstring.split("\n", 1)
        short_description = lines[0]

        if len(lines) > 1:
            long_description = lines[1].strip()

            params_returns_desc = None

            match = PARAM_OR_RETURNS_REGEX.search(long_description)
            if match:
                long_desc_end = match.start()
                params_returns_desc = long_description[long_desc_end:].strip()
                long_description = long_description[:long_desc_end].rstrip()

            if params_returns_desc:
                params = {
                    name: trim(doc)
                    for name, doc in PARAM_REGEX.findall(params_returns_desc)
                }

                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = reindent(match.group("doc"))

                # PARSES the COMSUMES (':consumes:') 'tag'
                match = CONSUMES_REGEX.findall(params_returns_desc)
                if match:
                    consumes = [
                        p[0]
                        for p in match
                    ]
                # PARSES the COMSUMES (':consumes:') 'tag'
                match = PRODUCES_REGEX.findall(params_returns_desc)
                if match:
                    produces = [
                        p[0]
                        for p in match
                    ]
                match = RAISES_REGEX.findall(params_returns_desc)
                if match:
                    raises = {
                        p[0]: p[2]
                        for p in match
                    }

                match = VERSION_REGEX.search(params_returns_desc)
                if match:
                    version = reindent(match.group().strip())

    ret = JsonObject(
        **{
            "summary": short_description,
            "description": long_description,
            "params": params,
            "returns": returns,
            "consumes": consumes,
            "produces": produces,
            "raises": raises,
            "version": version
        }
    )
    return ret


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    if '.' not in dotted_path:
        return import_module(dotted_path)
    else:

        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "{}" does not define a "{}" attribute/class'.format(
                dotted_path, class_name
            )
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def is_integer(value):
    try:
        value = int(value)
        return True
    except:
        return False