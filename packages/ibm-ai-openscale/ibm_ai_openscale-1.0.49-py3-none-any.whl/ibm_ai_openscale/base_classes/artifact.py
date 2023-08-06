from ibm_ai_openscale.utils import *

class JsonConvertable:
    def to_json(self):
        raise NotImplemented()

class Framework(JsonConvertable):
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def to_json(self):
        return {
            "name": self.name,
            "version": self.version
        }


# class Platform(JsonConvertable):
#     def __init__(self, name, version):
#         self.name = name
#         self.version = version
#
#     def to_json(self):
#         return {
#             "name": self.name,
#             "version": self.version
#         }


class Artifact(JsonConvertable):
    header = ['source_uid', 'source_url', 'binding_uid', 'name', 'type', 'created',
              'frameworks', 'source_entry']

    def __init__(self, source_uid, source_url, binding_uid, name, type, created, frameworks,
                 source_entry):
        validate_type(source_uid, "source_uid", str, True)
        validate_type(source_url, "source_url", str, False)
        validate_type(binding_uid, "binding_uid", str, True)
        validate_type(name, "name", str, True)
        validate_type(type, "type", str, True)
        validate_type(created, "created", str, True)
        validate_type(frameworks, "frameworks", list, True)
        validate_type(source_entry, "source_entry", dict, False)

        self.source_uid = source_uid
        self.source_url = source_url
        self.binding_uid = binding_uid
        self.name = name
        self.type = type
        self.created = created
        self.frameworks = frameworks
        self.source_entry = source_entry

    def to_json(self):
        j = {
            key: (self.__dict__[key] if not isinstance(self.__dict__[key], JsonConvertable) else self.__dict__[key].to_json())
            for key in self.__dict__ if not key.startswith('_')
        }

        j['frameworks'] = [f.to_json() for f in j['frameworks']]

        return j

