from woning.logger import Logger


class SmartHub:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.rules = []

    def add_rule(self, condition, action):
        self.rules.append((condition, action))

    def process_events(self, home):
        for rule in self.rules:
            condition, action = rule
            if condition(home):
                result = action(home)
                if result:
                    self.logger.log(result)
