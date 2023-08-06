class StorageReference:
    def __init__(self, credentials):
        self.credentials = credentials


class BluemixCloudObjectStorageReference(StorageReference):
    """
    Describes reference to file in COS.

    :param credentials: credentials to COS from Bluemix
    :type credentials: dict
    :param path: path within COS to file (bucket name + '/' + filename)
    :type path: str
    :param first_line_header: if csv, indicate if first row of file is header (optional)
    :type first_line_header: bool
    """
    def __init__(self, credentials, path, first_line_header=None):
        StorageReference.__init__(self, credentials)
        self.path = path
        self.first_line_header = first_line_header
