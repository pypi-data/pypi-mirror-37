from .instance import Instance

class DatabaseInstance(Instance):
    def __init__(self, credentials, database_type):
        Instance.__init__(self, credentials)
        self._database_type = database_type

    def _get_payload(self):
        return {
          "database_type": self._database_type,
          "credentials": self.credentials
        }