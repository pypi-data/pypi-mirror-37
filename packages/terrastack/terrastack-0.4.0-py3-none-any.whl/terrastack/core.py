# -*- coding: utf-8 -*-

import json, os
from string import Template

class QMarkTemplate(Template):
    delimiter = '?'

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge(value, node)
        elif isinstance(value, list) and isinstance(destination.get(key), list):
            destination[key].extend(value)
        else:
            destination[key] = value
    return destination

def load_environ_vars():
    return {k: v for k, v in os.environ.items() if k.startswith("VAR_")}

class Stack(object):
    def __init__(self, initial_components=[], var_dict={}):
        self.components = []
        self.var_dict = var_dict
        self.extend(*initial_components)

    def extend(self, *components):
        parsed_components = []
        for component in components:
            tmpl = QMarkTemplate(json.dumps(component.spec()))
            parsed_components.append(json.loads(tmpl.substitute(self.var_dict)))
        self.components.extend(parsed_components)

    def collate_to_dict(self):
        grouped_dict = {}
        for component in self.components:
            merge(component, grouped_dict)
        return grouped_dict

    def render_json(self):
        return json.dumps(self.collate_to_dict(), indent=4, sort_keys=True)

class Backend(object):
    def __init__(self, backend_type, **kwargs):
        self.backend_type = backend_type
        self.kwargs = kwargs
    def spec(self):
        return {
            "terraform": {
                "backend": {
                    self.backend_type: self.kwargs,
                }
            }
        }

class Provider(object):
    def __init__(self, provider_name, **kwargs):
        self.provider_name = provider_name
        self.kwargs = kwargs
    def spec(self):
        return {
            "provider": [{
                self.provider_name: self.kwargs,
            }]
        }

class Data(object):
    def __init__(self, data_type, data_name, **kwargs):
        self.data_type = data_type
        self.data_name = data_name
        self.kwargs    = kwargs
    def spec(self):
        return {
            "data": {
                self.data_type: {
                    self.data_name: self.kwargs,
                }
            }
        }

class Resource(object):
    def __init__(self, resource_type, resource_name, **kwargs):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.kwargs        = kwargs
    def spec(self):
        return {
            "resource": {
                self.resource_type: {
                    self.resource_name: self.kwargs,
                }
            }
        }

class Output(object):
    def __init__(self, output_name, output_value, **kwargs):
        self.output_name  = output_name
        self.output_value = output_value
        self.kwargs       = kwargs
    def spec(self):
        return {
            "output": {
                self.output_name: dict({
                        "value": self.output_value,
                    },
                    **self.kwargs,
                )
            }
        }

class Locals(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    def spec(self):
        return {
            "locals": self.kwargs,
        }

class Variable(object):
    def __init__(self, variable_name, **kwargs):
        self.variable_name = variable_name
        self.kwargs        = kwargs
    def spec(self):
        return {
            "variable": {
                self.variable_name: self.kwargs,
            }
        }
