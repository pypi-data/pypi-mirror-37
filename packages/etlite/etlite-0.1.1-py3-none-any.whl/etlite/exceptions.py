class TransformationError(RuntimeError):
    def __init__(self, message, record=None):
        super(TransformationError, self).__init__(message)
        self.record = record
