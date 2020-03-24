class ApiException(Exception):

    def __init__(self, api, message, trace):
        self.api = api
        self.message = message
        self.trace = trace

    def __str__(self):
        return "ApiException [{0}]: {1} \n{2}".format(self.api, self.message, self.trace)
