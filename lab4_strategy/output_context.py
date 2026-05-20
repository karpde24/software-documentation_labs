class OutputContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, data):
        self.strategy.output(data)
