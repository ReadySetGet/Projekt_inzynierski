"""Create a fuzzy inference system (fis) data model and edit its properties
(type, variables, membership functions (mf) and rules).

Classes:

    FISModel: data model class for a fis system

"""
import fuzzylab as fl
from fuzzylab.FuzzyInferenceSystem import FuzzyInferenceSystem
from modelsresources.fisrule_ext import FisRuleEx

DEFAULT_MF_PARAMS: dict[str, list] = {
    "gaussowska": [0.3196, 1.2467],
    "dzwonowa": [0.5, 3, 4],
    "trapezoidalna": [1, 3, 4, 4.5],
    "trójkątna": [2, 3, 4],
}
"""Default parameters for certain types of membership functions."""

MF_TYPE_TO_FUNCTION_NAME = {
    "gaussowska": "gaussmf",
    "dzwonowa": "gbellmf",
    "trójkątna": "trimf",
    "trapezoidalna": "trapmf",
}
"""Application-used name to library name membership function type converter."""

DEFAULT_IO_RANGE = [0, 5]
"""Default range of an input/output variable."""

DEFAULT_RULE_WEIGHT = 1
"""Default weight of a rule."""

DEFAULT_RULE_CONNECTION = 1
"""Default connection between variable conditions in a rule, 1 for AND, else 
for OR.
"""

DEFAULT_RULE_MF_INDEX = 1
"""Default membership function index to be used in rules with default settings.
1 means first mf, 0 means no condition for a given variable."""

DEFAULT_VARIABLE_TO_MF_MAPPING_BEHAVIOUR = 1
"""Default variable to membership function mapping behaviour when inferring.
1 means IS behaviour (mu(x) = mf(x)), else means IS NOT behaviour 
(mu(x) = 1 - mf(x)).
"""


class FISModel:
    """A class containing a fuzzy inference system (fis) and means of its
    edition. It allows modifying the system's properties (variables, mfs,
    rules).

    Attributes:

        _fis (FuzzyInferenceSystem): the contained fis system

    Methods:

        __init__(FuzzyInferenceSystem):
            Initialize a new class instance.
        add_input() -> None:
            Add a new input variable to the system.
        delete_input(int) -> int:
            Delete an input variable from the system.
        add_output() -> None:
            Add an output variable to the system.
        delete_output(int) -> int:
            Delete an output variable from the system.
        add_mf(str, str) -> int:
            Add a membership function to a variable.
        delete_mf(str, int) -> int:
            Delete a membership function from a variable.
        change_mf_type(str, int, str) -> int:
            Change the type of the given membership function.
        add_rule(list[int], list[int]) -> None:
            Add a rule to the system.
        delete_rule(int) -> int:
            Delete a rule from the system.
        clear_all_rules() -> None:
            Delete all rules.
        update_rule(int, list[int], list[int]) -> int:
            Update a given rule.
    """

    _fis: FuzzyInferenceSystem
    """The contained fis system."""

    def __init__(self, fis: FuzzyInferenceSystem = None):
        """Initialize a new class instance.

        Parameters:

            fis (FuzzyInferenceSystem): The fis system to be used. If None,
                a new Mamdani system will be generated.
        """
        if fis is None:
            self._fis = fl.mamfis("fis")
        else:
            self._fis = fis

    def add_input(self) -> None:
        """Add a new input variable to the system."""
        input_name = "input" + str(
            len(self._fis.Inputs) + 1)  # values like "input0", "input1"
        self._fis.addInput(DEFAULT_IO_RANGE, input_name)

    def delete_input(self, input_idx: int) -> int:
        """Delete an input variable from the system.

        Parameters:

            input_idx (int): index of the input to be deleted

        Returns:

            1 - input deleted correctly

            -1 - input with given index does not exist
        """
        if input_idx >= len(self._fis.Inputs):
            return -1
        self._fis.Inputs.pop(input_idx)
        return 1

    def add_output(self) -> None:
        """Add an output variable to the system."""
        output_name = "output" + str(len(self._fis.Outputs) + 1)
        self._fis.addOutput(DEFAULT_IO_RANGE, output_name)

    def delete_output(self, output_idx: int) -> int:
        """Delete an output variable from the system.

        Parameters:

            output_idx (int): index of the output to be deleted

        Returns:

            1 - output deleted correctly

            -1 - output with given index does not exist
        """
        if output_idx >= len(self._fis.Outputs):
            return -1
        self._fis.Outputs.pop(output_idx)
        return 1

    def add_mf(self, io_variable_name: str, mf_type: str = "trojkatna") -> int:
        """Add a membership function to a variable.

        Parameters:

            io_variable_name (str): name of the variable to add the mf to
            mf_type (str): type of the new mf, triangular by default

        Returns:

            1 - mf added successfully

            -1 - no io variable with the given name found

        """
        io_variable = self._find_variable(io_variable_name)
        if io_variable is None:
            return -1

        new_idx = len(io_variable.MembershipFunctions) + 1
        mf_name = "mf" + str(new_idx)
        self._fis.addMF(io_variable_name, MF_TYPE_TO_FUNCTION_NAME[mf_type],
                        DEFAULT_MF_PARAMS[mf_type], mf_name)
        return 1

    def delete_mf(self, io_variable_name: str, mf_idx: int) -> int:
        """Delete a membership function from a variable.

        Parameters:

            io_variable_name (str): name of the variable to delete the mf from
            mf_idx (int): index of the mf to be deleted

        Returns:

            1 - mf deleted correctly

            -1 - mf with the given index does not exist

            -2 - no io variable with a given name found
        """
        io_variable = self._find_variable(io_variable_name)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        io_variable.MembershipFunctions.pop(mf_idx)
        return 1

    def change_mf_type(self, io_variable_name: str, mf_idx: int,
                       new_mf_type: str) -> int:
        """Change the type of the given membership function.

        Parameters:

            io_variable_name (str): name of the variable containing the mf
            mf_idx (int): index of the mf to be changed
            new_mf_type (str): new type of the mf

        Returns:

            1 - mf type changed correctly

            -1 - mf with the given index does not exist

            -2 - no io variable with a given name found
        """
        io_variable = self._find_variable(io_variable_name)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        old_mf = io_variable.MembershipFunctions.pop(mf_idx)
        new_mf = fl.fismf(MF_TYPE_TO_FUNCTION_NAME[new_mf_type],
                          old_mf.Parameters, old_mf.Name)
        io_variable.MembershipFunctions.insert(mf_idx, new_mf)
        return 1

    def add_rule(self, is_mf: list[int] = None,
                 rule_data: list[int] = None) -> None:
        """Add a rule to the system.

        Parameters:

            is_mf (list[int]): list of variable to mf mapping behaviours when
                inferring (1 - use IS, else - use IS NOT)
                If None, IS values are used.
            rule_data (list[int]): list in a form of [imf1, imf2, imf3, ...,
                omf1, omf2, omf3, ... w, c], where:
                    imf1, imf2, imf3, ... - index of the mf to be used for the
                        input variable at a given list index
                    omf1, omf2, omf3, ... - index of the mf to be used for the
                        output variable at a given list index
                    w - weight of the rule

                    c - connector of variable conditions in the rule (1 - use
                        AND, else - use OR)
                If None, first mfs are used.
        """
        if rule_data is None:
            rule = [DEFAULT_RULE_MF_INDEX for _ in range(len(self._fis.Inputs)
                                                         + len(
                self._fis.Outputs))].extend(
                [DEFAULT_RULE_WEIGHT, DEFAULT_RULE_CONNECTION])
        else:
            rule = rule_data
        rule = [rule]

        if is_mf is None:
            is_mf_list = [DEFAULT_VARIABLE_TO_MF_MAPPING_BEHAVIOUR for _ in
                          range(len(self._fis.Inputs + self._fis.Outputs))]
        else:
            is_mf_list = is_mf
        self._fis.Rules.append(FisRuleEx(is_mf_list, rule,
                                         len(self._fis.Inputs)))

    def delete_rule(self, rule_idx: int) -> int:
        """Delete a rule from the system.

        Parameters:

            rule_idx (int): index of the rule to be deleted

        Returns:

            1 - rule deleted correctly

            -1 - rule with given index does not exist
        """
        if rule_idx >= len(self._fis.Rules):
            return -1
        self._fis.Rules.pop(rule_idx)

    def clear_all_rules(self) -> None:
        """Delete all rules."""
        self._fis.Rules.clear()

    def update_rule(self, rule_idx: int, new_rule_is_mf: list[int],
                    new_rule_data: list[int]) -> int:
        """Update a given rule.

            Parameters:

                rule_idx (int): index of the rule to be updated
                new_rule_is_mf (list[int]): list of variable to mf mapping
                    behaviours when inferring (1 - use IS, else - use IS NOT)
                new_rule_data (list[int]): list in a form of [imf1, imf2,
                    imf3, ..., omf1, omf2, omf3, ... w, c], where:
                        imf1, imf2, imf3, ... - index of the mf to be used for
                            the input variable at a given list index
                        omf1, omf2, omf3, ... - index of the mf to be used for
                            the output variable at a given list index
                        w - weight of the rule

                        c - connector of variable conditions in the rule
                            (1 - use AND, else - use OR)

            Returns:

                1 - rule updated correctly

                -1 - rule with given index does not exist
        """
        if rule_idx >= len(self._fis.Rules):
            return -1

        self._fis.Rules.pop(rule_idx)
        new_rule = FisRuleEx(new_rule_is_mf, [new_rule_data],
                             len(self._fis.Inputs))
        self._fis.Rules.insert(rule_idx, new_rule)
        return 1

    def _find_variable(self, io_variable_name: str) -> fl.fisvar:
        io_variable = None
        for idx in range(len(self._fis.Inputs)):
            if self._fis.Inputs[idx].Name == io_variable_name:
                io_variable = self._fis.Inputs[idx]
                break
        for idx in range(len(self._fis.Outputs)):
            if self._fis.Outputs[idx].Name == io_variable_name:
                io_variable = self._fis.Outputs[idx]
                break
        return io_variable
