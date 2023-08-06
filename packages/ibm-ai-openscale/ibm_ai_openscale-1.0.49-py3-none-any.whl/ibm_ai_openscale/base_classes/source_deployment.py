class SourceDeployment:
    def __init__(self, guid, url, name, deployment_type, created):
        self.guid = guid
        self.url = url
        self.name = name
        self.deployment_type = deployment_type
        self.created = created

    def _to_json(self):
        return {
            "deployment_id": self.guid,
            "url": self.url,
            "name": self.name,
            "deployment_type": self.deployment_type,
            "created_at": self.created
        }
