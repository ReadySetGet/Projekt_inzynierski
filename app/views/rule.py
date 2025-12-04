"""Rule class for fuzzy logic system."""


class Rule:
    """Represents a fuzzy logic rule in the system."""

    def __init__(
        self,
        input1,
        mf1,
        mf1_numb,
        input2,
        mf2,
        mf2_numb,
        output,
        mf3,
        mf3_numb,
        condition,
        connector,
        weight,
        name,
    ):
        """Initialize a fuzzy logic rule.

        Args:
            input1: First input variable name
            mf1: First input membership function name
            mf1_numb: First input membership function number
            input2: Second input variable name
            mf2: Second input membership function name
            mf2_numb: Second input membership function number
            output: Output variable name
            mf3: Output membership function name
            mf3_numb: Output membership function number
            condition: Condition type (is/is not)
            connector: Logical connector (and/or)
            weight: Rule weight
            name: Rule name
        """
        self._input1 = input1
        self._mf1 = mf1
        self._mf1_numb = mf1_numb
        self._input2 = input2
        self._mf2 = mf2
        self._mf2_numb = mf2_numb
        self._output = output
        self._mf3 = mf3
        self._mf3_numb = mf3_numb
        self._condition = condition
        self._connector = connector
        self._weight = weight
        self._name = name
        self._rule = (
            f"If {self._input1} {self._condition} {self._mf1} "
            f"{self._connector} {self._input2} {self._condition} "
            f"{self._mf2} then {self._output} is {self._mf3}"
        )

    def getName(self):
        """Get the rule name.

        Returns:
            Rule name
        """
        return self._name

    def getWeight(self):
        """Get the rule weight.

        Returns:
            Rule weight
        """
        return self._weight

    def getRule(self):
        """Get the rule text.

        Returns:
            Formatted rule text
        """
        return self._rule

    def getInputMfNumbers(self) -> str:
        """Get input membership function numbers.

        Returns:
            String containing input membership function numbers
        """
        if self._connector == "is not":
            result = f"-{self._mf1_numb} -{self._mf2_numb}"
        else:
            result = f"{self._mf1_numb} {self._mf2_numb}"
        return result

    def getOutputMfNumbers(self) -> str:
        """Get output membership function numbers.

        Returns:
            String containing output membership function numbers
        """
        if self._connector == "is not":
            result = f"-{self._mf3_numb}"
        else:
            result = f"{self._mf3_numb}"
        return result

    def getConnector(self) -> str:
        """Get connector code.

        Returns:
            "1" for "and", "2" for "or"
        """
        if self._connector == "and":
            return "1"
        else:
            return "2"
