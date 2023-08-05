class Handler:
    def __init__(self, inner, transformer=None, postProcessor=None):
        self.inner = inner
        self.transformer = transformer
        self.postProcessor = postProcessor

    def __call__(self, *args, **kwargs):
        if self.transformer is not None:
            args = (self.transformer(args[0]), args[1], args[0])

        result = self.inner(*args[0:2])
        if result is not None:
            kwargs.update({"innerResult": result})
        if self.postProcessor is not None:
            self.postProcessor(*args, **kwargs)
