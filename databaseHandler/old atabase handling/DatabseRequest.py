class DatabaseRequest:

    def __init__(self, request):
        self.request = request
        self.result = None
        self.errorMessage = None
        self.done = False


    def setErrorMessage(self, errorMessage):
        self.errorMessage = errorMessage

    def setResult(self, result):
        self.result = result