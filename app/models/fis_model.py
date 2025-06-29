import fuzzylab as fl
from fuzzylab.FuzzyInferenceSystem import FuzzyInferenceSystem

DEFAULT_MF_PARAMS: dict[str, list] = {
    "gaussowska": [0.3196, 1.2467],
    "dzwonowa": [0.5, 3, 4],
    "trapezoidalna": [1, 3, 4, 4.5],
    "trójkątna": [2, 3, 4],
}
MF_TYPE_TO_FUNCTION_NAME = {
    "gaussowska": "gaussmf",
    "dzwonowa": "gbellmf",
    "trójkątna": "trimf",
    "trapezoidalna": "trapmf",
}
DEFAULT_IO_FUNCTION_FIRST_PARAMETER_VALUES = [0, 5]
DEFAULT_RULE_WEIGHT = 1
DEFAULT_RULE_CONNECTION = 1
DEFAULT_RULE_MF_INDEX = 1  # fuzzylab counts mfs from 1 while adding rules


class FISModel:
    _fis: FuzzyInferenceSystem

    def __init__(self, fis: FuzzyInferenceSystem = None):
        if fis is None:
            self._fis = fl.mamfis("fis")
        else:
            self._fis = fis

    def add_input(self) -> None:
        input_name = "input" + str(
            len(self._fis.Inputs) + 1)  # values like "input0", "input1"
        self._fis.addInput(DEFAULT_IO_FUNCTION_FIRST_PARAMETER_VALUES,
                           Name=input_name)

    """
    1 - input deleted correctly
    -1 - input with a given index doesnt exist
    """
    def delete_input(self, input_idx: int) -> int:
        if input_idx >= len(self._fis.Inputs):
            return -1
        self._fis.Inputs.pop(input_idx)
        return 1

    def add_output(self) -> None:
        output_name = "output" + str(len(self._fis.Outputs) + 1)
        self._fis.addOutput(DEFAULT_IO_FUNCTION_FIRST_PARAMETER_VALUES,
                            Name=output_name)

    """
    1 - output deleted correctly
    -1 - output with a given index doesnt exist
    """
    def delete_output(self, output_idx: int) -> int:
        if output_idx >= len(self._fis.Outputs):
            return -1
        self._fis.Outputs.pop(output_idx)
        return 1

    """
    1 - added succesfully
    -1 - no io_variable named this way
    """
    def add_mf(self, io_variable_name: str, mf_type: str = "trojkatna") -> int:
        io_variable = None
        for idx in range(len(self._fis.Inputs)):
            if self._fis.Inputs[idx].Name == io_variable_name:
                io_variable = self._fis.Inputs[idx]
                break
        for idx in range(len(self._fis.Outputs)):
            if self._fis.Outputs[idx].Name == io_variable_name:
                io_variable = self._fis.Outputs[idx]
                break
        if io_variable is None:
            return -1

        new_idx = len(io_variable.MembershipFunctions) + 1
        mf_name = "mf" + str(new_idx)
        self._fis.addMF(io_variable_name, MF_TYPE_TO_FUNCTION_NAME[mf_type],
                        DEFAULT_MF_PARAMS[mf_type], Name=mf_name)
        return 1

    """
    1 - mf deleted correctly
    -1 - mf with a given index doesnt exist
    -2 - io with a given index doesnt exist
    """
    def delete_mf(self, mf_idx: int, io_idx: int, is_input: bool) -> int:
        if is_input:
            if io_idx >= len(self._fis.Inputs):
                return -2
            if mf_idx >= len(self._fis.Inputs[io_idx].MembershipFunctions):
                return -1
            self._fis.Inputs[io_idx].MembershipFunctions.pop(mf_idx)
        else:
            if io_idx >= len(self._fis.Outputs):
                return -2
            if mf_idx >= len(self._fis.Outputs[io_idx].MembershipFunctions):
                return -1
            self._fis.Outputs[io_idx].MembershipFunctions.pop(mf_idx)
        return 1

    def clear_all_rules(self) -> None:
        self._fis.Rules.clear()

    """
    rule_data: a list in a form of [imf1, imf2, imf3, ..., omf1, omf2, omf3, ... w, c], where:
    x, y, z, ... - nr of mf of an input of a given (list) index
    o - nr of nr of mf of an input of a given (list) index
    w - weight of rule
    c - connection of rule
    """
    def add_rule(self, rule_data: list[int] = None) -> None:
        if rule_data is None:
            rule = [DEFAULT_RULE_MF_INDEX for _ in range(len(self._fis.Inputs)
                                                         + len(
                self._fis.Outputs))].extend(
                [DEFAULT_RULE_WEIGHT, DEFAULT_RULE_CONNECTION])
        else:
            rule = rule_data
        self._fis.addRule(rule)

    """
    1 - rule deleted correctly
    -1 - rule with given idx doesnt exist
    """
    def delete_rule(self, rule_idx: int) -> int:
        if rule_idx >= len(self._fis.Rules):
            return -1
        self._fis.Rules.pop(rule_idx)
