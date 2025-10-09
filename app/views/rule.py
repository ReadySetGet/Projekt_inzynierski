class Rule:
    """Placeholder helper class meant to simulate a structure of a rule in the system."""
    def __init__(self, input1, mf1, input2, mf2, output, mf3, condition, connector, weight, name):
        self._input1 = input1
        self._mf1 = mf1
        self._input2 = input2
        self._mf2 = mf2
        self._output = output
        self._mf3 = mf3
        self._condition = condition
        self._connector = connector
        self._weight = weight
        self._name = name
        self._rule = (f"If {self._input1} {self._condition} {self._mf1} {self._connector} {self._input2}"
                      f" {self._condition} {self._mf2} then {self._output} is {self._mf3}")

    def getName(self):
        return self._name

    def getWeight(self):
        return self._weight

    def getRule(self):
        return self._rule