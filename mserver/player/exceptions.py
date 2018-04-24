class MServerException(Exception):
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.context = context
        super().__init__(*args, **kwargs)
