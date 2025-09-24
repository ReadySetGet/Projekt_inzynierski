"""Create a fuzzy inference system (fis) data model and edit its properties
(type, variables, membership functions (mf) and rules).

Classes:

    FISModel: data model class for a fis system

"""
import fuzzylab as fl
from fuzzylab.FuzzyInferenceSystem import FuzzyInferenceSystem
from .modelsresources.fisrule_ext import FisRuleEx

DEFAULT_MF_PARAMS: dict[str, list] = {
    "gaussowska": [0.3196, 1.2467],
    "dzwonowa": [0.5, 3, 4],
    "trojkatna": [0, 0.5, 1],
    "trapezoidalna": [1, 3, 4, 4.5],
    "stala": 0.5,
}
"""Default parameters for certain types of membership functions."""

DEFAULT_MF_PARAMS_SUGENO: dict[str, list | float] = {
    "stala": 0.5,
    "liniowa": [1, 1, 0.5],
}
"""Default parameters for certain types of membership functions, for Sugeno
output variables.
"""

MF_TYPE_TO_FUNCTION_NAME = {
    "gaussowska": "gaussmf",
    "dzwonowa": "gbellmf",
    "trojkatna": "trimf",
    "trapezoidalna": "trapmf",
}
"""Application-used name to library name membership function type converter."""

MF_TYPE_TO_FUNCTION_NAME_SUGENO = {
    "stala": "constant",
    "liniowa": "linear",
}
"""Application-used name to library name membership function type converter,
for Sugeno output variables.
"""

DEFAULT_IO_RANGE = [0, 1]
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

RESOLUTION_OF_VARIABLE_RANGE = 0.01
"""Acceptable resolution of variable range values."""


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

    _fis: fl.mamfis | fl.sugfis
    """The contained fis system."""

    def __init__(self, fis: fl.mamfis | fl.sugfis = None):
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
        next_input_number = self._find_available_element_number("input")
        input_name = "input" + str(
            next_input_number)  # values like "input0", "input1"
        self._fis.addInput(DEFAULT_IO_RANGE, Name=input_name)

        for rule in self._fis.Rules:
            rule.numInputs += 1
            rule.Antecedent.append(0)

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

        rules_to_be_deleted_idx = []
        for rule_idx in range(len(self._fis.Rules)):
            if self._fis.Rules[rule_idx].Antecedent[input_idx] == 0:
                self._fis.Rules[rule_idx].Antecedent.pop(input_idx)
                self._fis.Rules[rule_idx].numInputs -= 1
            else:
                nr_of_none_variables = self._fis.Rules[rule_idx].Antecedent \
                    .count(0)
                nr_of_not_none_variables = len(self._fis.Rules[rule_idx]
                                               .Antecedent) \
                                               - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    self._fis.Rules[rule_idx].Antecedent.pop(input_idx)
                    self._fis.Rules[rule_idx].numInputs -= 1
                else:
                    rules_to_be_deleted_idx.append(rule_idx)

        for rule_idx in rules_to_be_deleted_idx:
            self._fis.Rules.pop(rule_idx)

        return 1

    def add_output(self) -> None:
        """Add an output variable to the system."""
        next_output_number = self._find_available_element_number("output")
        output_name = "output" + str(next_output_number)
        self._fis.addOutput(DEFAULT_IO_RANGE, Name=output_name)

        for rule in self._fis.Rules:
            rule.Consequent.append(0)

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

        rules_to_be_deleted_idx = []
        for rule_idx in range(len(self._fis.Rules)):
            if self._fis.Rules[rule_idx].Consequent[output_idx] == 0:
                self._fis.Rules[rule_idx].Consequent.pop(output_idx)
            else:
                nr_of_none_variables = self._fis.Rules[rule_idx].Consequent \
                    .count(0)
                nr_of_not_none_variables = len(self._fis.Rules[rule_idx]
                                               .Consequent) \
                                               - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    self._fis.Rules[rule_idx].Consequent.pop(output_idx)
                else:
                    rules_to_be_deleted_idx.append(rule_idx)

        for rule_idx in rules_to_be_deleted_idx:
            self._fis.Rules.pop(rule_idx)

        return 1

    def add_mf(self, io_variable_name: str, input_or_output: str,
               mf_type: str = "trojkatna") -> int:
        """Add a membership function to a variable.

        Parameters:

            io_variable_name (str): name of the variable to add the mf to
            input_or_output (str): "input" if the variable is an input,
                "output" if else
            mf_type (str): type of the new mf, triangular by default

        Returns:

            1 - mf added successfully

            -1 - no io variable with the given name found

            -2 - mf type provided not available for the inference type used
                and/or variable type provided

        """
        [io_variable, _] = self._find_variable(io_variable_name,
                                               input_or_output)
        if io_variable is None:
            return -1

        next_mf_number = self._find_available_element_number("mf", io_variable)
        mf_name = "mf" + str(next_mf_number)

        mf_adding_validity_check = self._check_if_new_mf_type_is_valid(input_or_output,
                                                                       mf_type)
        if not mf_adding_validity_check[0]:
            return -2

        self._fis.addMF(io_variable_name, mf_adding_validity_check[1],
                        mf_adding_validity_check[2], Name=mf_name)

        return 1

    def delete_mf(self, io_variable_name: str, input_or_output: str,
                  mf_idx: int) -> int:
        """Delete a membership function from a variable.

        Parameters:

            io_variable_name (str): name of the variable to delete the mf from
            input_or_output (str): "input" if the variable is an input,
                "output" if else
            mf_idx (int): index of the mf to be deleted

        Returns:

            1 - mf deleted correctly

            -1 - mf with the given index does not exist

            -2 - no io variable with a given name found
        """
        [io_variable, io_variable_idx] = self._find_variable(io_variable_name,
                                                             input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        io_variable.MembershipFunctions.pop(mf_idx)

        rules_to_be_deleted_idx = []
        search_list = []
        for rule_idx in range(len(self._fis.Rules)):
            if input_or_output == "input":
                search_list = self._fis.Rules[rule_idx].Antecedent
            if input_or_output == "output":
                search_list = self._fis.Rules[rule_idx].Consequent

            if search_list[io_variable_idx] == mf_idx:
                nr_of_none_variables = search_list.count(0)
                nr_of_not_none_variables = len(search_list) \
                                           - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    search_list.pop(io_variable_idx)
                    if input_or_output == "input":
                        self._fis.Rules[rule_idx].numInputs -= 1
                else:
                    rules_to_be_deleted_idx.append(rule_idx)

        for rule_idx in rules_to_be_deleted_idx:
            self._fis.Rules.pop(rule_idx)

        return 1

    def change_mf_type(self, io_variable_name: str, input_or_output: str,
                       mf_idx: int, new_mf_type: str) -> int:
        """Change the type of the given membership function.

        Parameters:

            io_variable_name (str): name of the variable containing the mf
            input_or_output (str): "input" if the variable is an input,
                "output" if else
            mf_idx (int): index of the mf to be changed
            new_mf_type (str): new type of the mf

        Returns:

            1 - mf type changed correctly

            -1 - mf with the given index does not exist

            -2 - no io variable with a given name found

            -3 - mf type provided not available for the inference type used
                and/or variable type provided
        """
        [io_variable, _] = self._find_variable(io_variable_name,
                                               input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        mf_changing_validity_check = self._check_if_new_mf_type_is_valid(input_or_output,
                                                                         new_mf_type)
        if not mf_changing_validity_check[0]:
            return -3

        old_mf = io_variable.MembershipFunctions.pop(mf_idx)
        new_mf = fl.fismf(mf_changing_validity_check[1],
                          mf_changing_validity_check[2], old_mf.Name)
        io_variable.MembershipFunctions.insert(mf_idx, new_mf)
        return 1

    def add_rule(self, is_mf: list[int] = None,
                 rule_data: list[int] = None) -> int:
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

        Returns:

            1 - rule added successfully

            -1 - all provided inputs or all provided outputs have mfs set to
                None

            -2 - not all input/output variables have mfs added (at least 1 is
                mandatory)

            -3 - output variables in Sugeno inference cannot have IS NOT
                behaviour - incorrect data provided
        """
        if not self._check_if_every_variable_has_mf():
            return -2

        if rule_data is None:
            rule = []
            rule.append(DEFAULT_RULE_MF_INDEX)
            for _ in range(len(self._fis.Inputs) - 1):
                rule.append(0)

            rule.append(DEFAULT_RULE_MF_INDEX)
            for _ in range(len(self._fis.Outputs) - 1):
                rule.append(0)

            rule.append(DEFAULT_RULE_WEIGHT)
            rule.append(DEFAULT_RULE_CONNECTION)
        else:
            rule = rule_data
            rule_for_input = rule[:len(self._fis.Inputs)]
            rule_for_output = rule[len(self._fis.Inputs):]
            if len(rule_for_input) - rule_for_input.count(0) == 0:
                return -1
            if len(rule_for_output) - rule_for_output.count(0) == 0:
                return -1

        rule = [rule]

        if is_mf is None:
            is_mf_list = [DEFAULT_VARIABLE_TO_MF_MAPPING_BEHAVIOUR for _ in
                          range(len(self._fis.Inputs + self._fis.Outputs))]
        else:
            if not self._check_if_is_behaviour_list_is_valid(is_mf):
                return -3
            is_mf_list = is_mf

        new_rule_name = "rule" \
                        + str(self._find_available_element_number("rule"))
        self._fis.Rules.append(FisRuleEx(is_mf_list, new_rule_name, rule,
                                         len(self._fis.Inputs)))
        return 1

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

                -2 - new weight not in [0, 1]

                -3 - the lists provided are of wrong length

                -4 - output variables in Sugeno inference cannot have IS NOT
                behaviour - incorrect data provided
        """
        if rule_idx >= len(self._fis.Rules):
            return -1

        if new_rule_data[-2] < 0 or new_rule_data[-2] > 1:
            return -2

        if len(new_rule_is_mf) != len(self._fis.Inputs) \
            + len(self._fis.Outputs):
            return -3
        if len(new_rule_data) != len(self._fis.Inputs) \
            + len(self._fis.Outputs) + 2:
            return -3

        if not self._check_if_is_behaviour_list_is_valid(new_rule_is_mf):
            return -4

        self._fis.Rules.pop(rule_idx)

        new_rule_name = "rule" \
                        + str(self._find_available_element_number("rule"))
        new_rule = FisRuleEx(new_rule_is_mf, new_rule_name, [new_rule_data],
                             len(self._fis.Inputs))
        self._fis.Rules.insert(rule_idx, new_rule)
        return 1

    def change_variable_range(self, io_variable_name: str,
                              input_or_output: str,
                              new_range: list[float]) -> int:
        """Change the domain range of a given input/output variable.

        Parameters:

            io_variable_name (str): name of the variable
            input_or_output (str): "input" if the variable is an input,
                "output" if else
            new_range (list[int]): new range for the variable, in the form of
                [min, max]

        Returns:

            1 - range changed successfully

            -1 - provided min is higher than provided max

            -2 - range values are stricter than acceptable resolution
        """
        if new_range[0] >= new_range[1]:
            return -1

        if round(new_range[0]/RESOLUTION_OF_VARIABLE_RANGE) \
                - new_range[0]/RESOLUTION_OF_VARIABLE_RANGE != 0:
            return -2

        if round(new_range[1] / RESOLUTION_OF_VARIABLE_RANGE) \
                - new_range[1] / RESOLUTION_OF_VARIABLE_RANGE != 0:
            return -2

        [io_variable, io_idx] = self._find_variable(io_variable_name,
                                                    input_or_output)
        self._fis.Inputs.pop(io_idx)
        io_variable.Range = new_range
        self._fis.Inputs.insert(io_idx, io_variable)
        return 1

    def _find_variable(self, io_variable_name: str,
                       input_or_output: str) -> [fl.fisvar, int]:
        io_variable = None
        found_idx = -1
        search_list = []
        if input_or_output == "input":
            search_list = self._fis.Inputs
        if input_or_output == "output":
            search_list = self._fis.Outputs

        for idx in range(len(search_list)):
            if search_list[idx].Name == io_variable_name:
                io_variable = search_list[idx]
                found_idx = idx
                break

        return io_variable, found_idx

    def _find_available_element_number(self, element_type: str,
                                       io_variable: fl.fisvar = None) -> int:
        search_list = []
        if element_type == "input":
            search_list = self._fis.Inputs
        if element_type == "output":
            search_list = self._fis.Outputs
        if element_type == "mf":
            search_list = io_variable.MembershipFunctions
        if element_type == "rule":
            search_list = self._fis.Rules

        names = [el.Name for el in search_list]

        potential_nr = 0
        while True:
            exists = names.count(element_type + str(potential_nr))
            if exists == 0:
                break
            potential_nr += 1

        return potential_nr

    def _check_if_every_variable_has_mf(self) -> bool:
        for variable in self._fis.Inputs + self._fis.Outputs:
            if len(variable.MembershipFunctions) == 0:
                return False

        return True

    def _check_if_new_mf_type_is_valid(self, input_or_output: str,
                                       mf_type: str) -> [bool, str,
                                                         list | int]:
        if type(self._fis) is fl.mamfis:
            if mf_type not in MF_TYPE_TO_FUNCTION_NAME.keys():
                return [False, "", -1]
            return [True, MF_TYPE_TO_FUNCTION_NAME[mf_type],
                    DEFAULT_MF_PARAMS[mf_type]]

        if type(self._fis) is fl.sugfis:
            if input_or_output == "input":
                if mf_type not in MF_TYPE_TO_FUNCTION_NAME.keys():
                    return [False, "", -1]
                return [True, MF_TYPE_TO_FUNCTION_NAME[mf_type],
                        DEFAULT_MF_PARAMS[mf_type]]
            if input_or_output == "output":
                if mf_type not in MF_TYPE_TO_FUNCTION_NAME_SUGENO.keys():
                    return [False, "", -1]
                return [True, MF_TYPE_TO_FUNCTION_NAME_SUGENO[mf_type],
                        DEFAULT_MF_PARAMS_SUGENO[mf_type]]

    def _check_if_is_behaviour_list_is_valid(self, is_mf: list[int]) -> bool:
        if type(self._fis) is fl.sugfis:
            check_if_correct_for_sugeno = is_mf[len(self._fis.Inputs):]
            if check_if_correct_for_sugeno.count(1) != len(
                    check_if_correct_for_sugeno):
                return False

        return True
