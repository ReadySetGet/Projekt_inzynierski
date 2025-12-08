"""Create a fuzzy inference system (fis) data model and edit its properties.

This module handles type, variables, membership functions (mf) and rules.

Classes:

    FISModel: data model class for a fis system
"""

import itertools
from typing import Self

import fuzzylab as fl

from .modelsresources.fisrule_ext import FisRuleEx

DEFAULT_MF_PARAMS: dict[str, list] = {
    "gaussowska": [0.3196, 1.2467],
    "dzwonowa": [0.5, 3, 4],
    "trojkatna": [0, 0.5, 1],
    "trapezoidalna": [1, 3, 4, 4.5],
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

AVAILABLE_LOGIC_METHODS_MAMDANI: dict[str, list[str]] = {
    "AndMethod": ["min", "prod"],
    "OrMethod": ["max", "probor", "sum"],
    "ImplicationMethod": ["min", "prod"],
    "AggregationMethod": ["max", "probor", "sum"],
}
"""Available logic methods for certain functions of Mamdani fis."""

AVAILABLE_LOGIC_METHODS_SUGENO: dict[str, list[str]] = {
    "AndMethod": ["min", "prod"],
    "OrMethod": ["max", "probor", "sum"],
    "ImplicationMethod": ["prod"],
    "AggregationMethod": ["sum"],
}
"""Available logic methods for certain functions of Sugeno fis."""

AVAILABLE_DEFUZZIFICATION_METHODS = ["centroid", "bisector", "mom", "som", "lom"]
"""Available defuzzification methods."""

AVAILABLE_DEFUZZIFICATION_METHODS_SUGENO = ["wtaver"]
"""Available defuzzification methods for Sugeno inference."""

MF_NAME_MAX_LENGTH: int = 100
"""Max length of a membership function's name."""

MF_PARAMETER_LENGTH_PER_TYPE: dict[str, int] = {
    "gaussmf": 2,
    "gbellmf": 3,
    "trimf": 3,
    "trapmf": 4,
    "constant": 1,
    "linear": 3,
}
"""Parameter list length for each given mf type."""

NR_OF_INTERPOLATION_POINTS_MIN = 10
"""Default minimum number of function interpolation points."""

NR_OF_INTERPOLATION_POINTS_MAX = 1000
"""Default maximum number of function interpolation points."""

DEFAULT_INTERPOLATION_POINTS_NUMBER = 100
"""Default number of function interpolation points."""

RESOLUTION_OF_VARIABLE_RANGE = 0.01
"""Acceptable resolution of variable range values."""


class FISModel:
    """A class containing a fuzzy inference system (fis) and means of its edition.

    It allows modifying the system's properties (variables, mfs, rules).
    """

    _fis: fl.mamfis | fl.sugfis
    """The contained fis system."""
    _interpolation_points_nr: int
    """Nr of function interpolation points."""

    def __init__(
        self,
        fis: fl.mamfis | fl.sugfis = None,
        fis_name: str = "fis",
        fis_type: str = None,
        int_points: int = DEFAULT_INTERPOLATION_POINTS_NUMBER,
    ):
        """Initialize the model with an existing or freshly created FIS.

        Parameters
        ----------
        fis : fl.mamfis | fl.sugfis | None
            The fuzzy inference system to wrap. When ``None``, a new system is
            created.
        fis_name : str
            Name to apply when a new system instance is generated.
        fis_type : str | None
            Type of system to create when ``fis`` is ``None``. Accepted values
            are ``"mamdani"`` and ``"sugeno"``. When omitted a Mamdani system
            is created by default.
        int_points : int
            Number of function interpolation points, by default 100.
        """
        self._interpolation_points_nr = int_points
        if fis_type is not None:
            if fis_type == "sugeno":
                self._fis = fl.sugfis(fis_name)
            if fis_type == "mamdani":
                self._fis = fl.mamfis(fis_name)
        elif fis is None:
            self._fis = fl.mamfis(fis_name)
        else:
            self._fis = fis
            self._normalize_rule_names()

    def _normalize_rule_names(self) -> None:
        """Normalize rule names to ensure they are unique (rule1, rule2, etc.).

        This is called when loading a FIS from file to fix cases where
        multiple rules have the same name (e.g., all named "Rule").
        """
        if not hasattr(self._fis, "Rules") or not self._fis.Rules:
            return

        rule_names = [rule.Name if hasattr(rule, "Name") else "Rule" for rule in self._fis.Rules]
        name_counts = {}
        for name in rule_names:
            name_counts[name] = name_counts.get(name, 0) + 1

        has_duplicates = any(count > 1 for count in name_counts.values())
        if has_duplicates:
            for i, rule in enumerate(self._fis.Rules):
                new_name = f"rule{i + 1}"
                try:
                    rule.Name = new_name
                except Exception:
                    setattr(rule, "Name", new_name)

    def add_input(self) -> None:
        """Add a new input variable to the system."""
        next_input_number = self._find_available_element_number("input")
        input_name = "input" + str(next_input_number)
        self._fis.addInput(DEFAULT_IO_RANGE, Name=input_name)

        for rule in self._fis.Rules:
            rule.Antecedent.append(0)

    def delete_input(self, input_idx: int) -> int:
        """Delete an input variable from the system.

        Args:
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
            else:
                nr_of_none_variables = self._fis.Rules[rule_idx].Antecedent.count(0)
                nr_of_not_none_variables = len(self._fis.Rules[rule_idx].Antecedent) - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    self._fis.Rules[rule_idx].Antecedent.pop(input_idx)
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

        Args:
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
                nr_of_none_variables = self._fis.Rules[rule_idx].Consequent.count(0)
                nr_of_not_none_variables = len(self._fis.Rules[rule_idx].Consequent) - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    self._fis.Rules[rule_idx].Consequent.pop(output_idx)
                else:
                    rules_to_be_deleted_idx.append(rule_idx)

        for rule_idx in rules_to_be_deleted_idx:
            self._fis.Rules.pop(rule_idx)

        return 1

    def add_mf(self, io_variable_name: str, input_or_output: str, mf_type: str = "trojkatna") -> int:
        """Add a membership function to a variable.

        Args:
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
        [io_variable, _] = self._find_variable(io_variable_name, input_or_output)
        if io_variable is None:
            return -1

        next_mf_number = self._find_available_element_number("mf", io_variable)
        mf_name = "mf" + str(next_mf_number)

        mf_adding_validity_check = self._check_if_new_mf_type_is_valid(input_or_output, mf_type)
        if not mf_adding_validity_check[0]:
            return -2

        self._fis.addMF(
            io_variable_name,
            mf_adding_validity_check[1],
            mf_adding_validity_check[2],
            Name=mf_name,
        )

        return 1

    def delete_mf(self, io_variable_name: str, input_or_output: str, mf_idx: int) -> int:
        """Delete a membership function from a variable.

        Args:
            io_variable_name (str): name of the variable to delete the mf from
            input_or_output (str): "input" if the variable is an input,
                "output" if else
            mf_idx (int): index of the mf to be deleted

        Returns:
            1 - mf deleted correctly
            -1 - mf with the given index does not exist
            -2 - no io variable with a given name found
        """
        [io_variable, io_variable_idx] = self._find_variable(io_variable_name, input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        io_variable.MembershipFunctions.pop(mf_idx)

        rules_to_be_deleted_idx = []
        for rule_idx in range(len(self._fis.Rules)):
            search_list = None
            if input_or_output == "input":
                search_list = self._fis.Rules[rule_idx].Antecedent
            elif input_or_output == "output":
                search_list = self._fis.Rules[rule_idx].Consequent

            if search_list is None or io_variable_idx >= len(search_list):
                continue

            current_mf_ref = search_list[io_variable_idx]

            if current_mf_ref == mf_idx:
                nr_of_none_variables = search_list.count(0)
                nr_of_not_none_variables = len(search_list) - nr_of_none_variables
                if nr_of_not_none_variables > 1:
                    search_list[io_variable_idx] = 0
                else:
                    rules_to_be_deleted_idx.append(rule_idx)
            elif current_mf_ref > mf_idx:
                search_list[io_variable_idx] = current_mf_ref - 1

        for rule_idx in sorted(rules_to_be_deleted_idx, reverse=True):
            self._fis.Rules.pop(rule_idx)

        return 1

    def change_mf_type(self, io_variable_name: str, input_or_output: str, mf_idx: int, new_mf_type: str) -> int:
        """Change the type of the given membership function.

        Args:
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
        [io_variable, _] = self._find_variable(io_variable_name, input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        mf_changing_validity_check = self._check_if_new_mf_type_is_valid(input_or_output, new_mf_type)
        if not mf_changing_validity_check[0]:
            return -3

        old_mf = io_variable.MembershipFunctions[mf_idx]

        try:
            old_mf.Type = mf_changing_validity_check[1]
            old_mf.Parameters = mf_changing_validity_check[2]
        except Exception:
            old_mf = io_variable.MembershipFunctions.pop(mf_idx)
            new_mf = fl.fismf(
                mf_changing_validity_check[1],
                mf_changing_validity_check[2],
            )
            try:
                new_mf.Name = old_mf.Name
            except Exception:
                setattr(new_mf, "Name", old_mf.Name)
            io_variable.MembershipFunctions.insert(mf_idx, new_mf)
        return 1

    def add_rule(self, is_mf: list[int] = None, rule_data: list[int] = None) -> int:
        """Add a rule to the system.

        Args:
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
            print("Error in add_rule: Not all variables have MFs")
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
            rule_for_input = rule[: len(self._fis.Inputs)]
            rule_for_output = rule[len(self._fis.Inputs) : len(self._fis.Inputs) + len(self._fis.Outputs)]
            if len(rule_for_input) - rule_for_input.count(0) == 0:
                print(f"Error in add_rule: All inputs are 0. rule_for_input={rule_for_input}")
                return -1
            if len(rule_for_output) - rule_for_output.count(0) == 0:
                print(f"Error in add_rule: All outputs are 0. rule_for_output={rule_for_output}")
                return -1

        rule = [rule]

        if is_mf is None:
            is_mf_list = [
                DEFAULT_VARIABLE_TO_MF_MAPPING_BEHAVIOUR for _ in range(len(self._fis.Inputs + self._fis.Outputs))
            ]
        else:
            if not self._check_if_is_behaviour_list_is_valid(is_mf):
                return -3
            is_mf_list = is_mf

        new_rule_name = "rule" + str(self._find_available_element_number("rule"))
        self._fis.Rules.append(FisRuleEx(is_mf_list, new_rule_name, rule, len(self._fis.Inputs)))
        return 1

    def delete_rule(self, rule_idx: int) -> int:
        """Delete a rule from the system.

        Args:
            rule_idx (int): index of the rule to be deleted

        Returns:
            1 - rule deleted correctly
            -1 - rule with given index does not exist
        """
        if rule_idx >= len(self._fis.Rules):
            return -1
        self._fis.Rules.pop(rule_idx)
        return 1

    def clear_all_rules(self) -> None:
        """Delete all rules from the system."""
        self._fis.Rules.clear()

    def update_rule(self, rule_idx: int, new_rule_is_mf: list[int], new_rule_data: list[int]) -> int:
        """Update a given rule.

        Args:
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

        if len(new_rule_is_mf) != len(self._fis.Inputs) + len(self._fis.Outputs):
            return -3
        if len(new_rule_data) != len(self._fis.Inputs) + len(self._fis.Outputs) + 2:
            return -3

        if not self._check_if_is_behaviour_list_is_valid(new_rule_is_mf):
            return -4

        old_rule = self._fis.Rules[rule_idx]
        old_rule_name = old_rule.Name if hasattr(old_rule, "Name") else "rule" + str(rule_idx)
        self._fis.Rules.pop(rule_idx)

        new_rule = FisRuleEx(new_rule_is_mf, old_rule_name, [new_rule_data], len(self._fis.Inputs))
        self._fis.Rules.insert(rule_idx, new_rule)
        return 1

    def update_logic_methods(
        self, and_method: str = "", or_method: str = "", imp_method: str = "", agg_method: str = ""
    ) -> int:
        """Update the logic methods (and, or, implication, aggregation) of the fis used.

        Pass only those methods you want changed.

        Args:
            and_method (str): New AND method to use.
            or_method (str): New OR method to use.
            imp_method (str): New implication method to use.
            agg_method (str): New aggregation method to use.

        Returns:
            int: 1 if updates made successfully, -1 if new method provided not available
                for the fis type used or incorrect.
        """
        methods_list = []
        if type(self._fis) is fl.mamfis:
            methods_list = AVAILABLE_LOGIC_METHODS_MAMDANI
        if type(self._fis) is fl.sugfis:
            methods_list = AVAILABLE_LOGIC_METHODS_SUGENO

        if and_method != "":
            if and_method not in methods_list["AndMethod"]:
                return -1
            self._fis.AndMethod = and_method
        if or_method != "":
            if or_method not in methods_list["OrMethod"]:
                return -1
            self._fis.OrMethod = or_method
        if imp_method != "":
            if imp_method not in methods_list["ImplicationMethod"]:
                return -1
            self._fis.ImplicationMethod = imp_method
        if agg_method != "":
            if agg_method not in methods_list["AggregationMethod"]:
                return -1
            self._fis.AggregationMethod = agg_method

        return 1

    def change_defuzzification_method(self, new_method: str) -> int:
        """Change defuzzification method used.

        Args:
            new_method (str): New defuzzification method to be used. Available
                options: centroid, bisector, mom, som, lom, wtaver.

        Returns:
            int: 1 if method changed successfully, -1 if new method provided not in
                available methods.
        """
        if type(self._fis) is fl.mamfis:
            if new_method not in AVAILABLE_DEFUZZIFICATION_METHODS:
                return -1

        if type(self._fis) is fl.sugfis:
            if new_method not in AVAILABLE_DEFUZZIFICATION_METHODS_SUGENO:
                return -1

        self._fis.DefuzzificationMethod = new_method
        return 1

    def change_mf_name(self, io_variable_name: str, input_or_output: str, mf_idx: int, new_mf_name: str) -> int:
        """Change the name of the given membership function.

        Args:
            io_variable_name (str): Name of the variable containing the mf.
            input_or_output (str): "input" if the variable is an input, "output" if else.
            mf_idx (int): Index of the mf to be changed.
            new_mf_name (str): New name of the mf.

        Returns:
            int: 1 if mf name changed correctly, -1 if mf with the given index does not exist,
                -2 if no io variable with a given name found, -3 if mf name too long.
        """
        if len(new_mf_name) > MF_NAME_MAX_LENGTH:
            return -3

        [io_variable, _] = self._find_variable(io_variable_name, input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        io_variable.MembershipFunctions[mf_idx].Name = new_mf_name
        return 1

    def change_mf_parameters(
        self, io_variable_name: str, input_or_output: str, mf_idx: int, new_mf_parameters: list[float] | int
    ) -> int:
        """Change the parameters of the given membership function.

        Args:
            io_variable_name (str): Name of the variable containing the mf.
            input_or_output (str): "input" if the variable is an input, "output" if else.
            mf_idx (int): Index of the mf to be changed.
            new_mf_parameters (list[float] | int): New parameters of the mf.

        Returns:
            int: 1 if mf parameters changed correctly, -1 if mf with the given index does not exist,
                -2 if no io variable with a given name found, -3 if parameter list is too long or
                too short for the mf type used, or parameters for constant used for other mf type.
        """
        [io_variable, _] = self._find_variable(io_variable_name, input_or_output)
        if io_variable is None:
            return -2

        if mf_idx >= len(io_variable.MembershipFunctions):
            return -1

        if type(new_mf_parameters) is list:
            if (
                len(new_mf_parameters) != MF_PARAMETER_LENGTH_PER_TYPE[io_variable.MembershipFunctions[mf_idx].Type]
                or io_variable.MembershipFunctions[mf_idx].Type == "constant"
            ):
                return -3
        else:
            if io_variable.MembershipFunctions[mf_idx].Type != "constant":
                return -3

        io_variable.MembershipFunctions[mf_idx].Parameters = new_mf_parameters
        return 1

    def set_interpolation_points(self, new_val: int) -> int:
        """Set the number of function interpolation points.

        Args:
            new_val (int): New number of function interpolation points.

        Returns:
            int: 1 if value changed successfully, -1 if value lower or higher than set border values.
        """
        if new_val < NR_OF_INTERPOLATION_POINTS_MIN or new_val > NR_OF_INTERPOLATION_POINTS_MAX:
            return -1

        self._interpolation_points_nr = new_val
        return 1

    def get_interpolation_points(self) -> int:
        """Get the function interpolation points number."""
        return self._interpolation_points_nr

    def change_variable_range(self, io_variable_name: str, input_or_output: str, new_range: list[float]) -> int:
        """Change the domain range of a given input/output variable.

        Args:
            io_variable_name (str): Name of the variable.
            input_or_output (str): "input" if the variable is an input, "output" if else.
            new_range (list[float]): New range for the variable, in the form of [min, max].

        Returns:
            int: 1 if range changed successfully, -1 if provided min is higher than provided max,
                -2 if range values are stricter than acceptable resolution.
        """
        if new_range[0] >= new_range[1]:
            return -1

        if round(new_range[0] / RESOLUTION_OF_VARIABLE_RANGE) - new_range[0] / RESOLUTION_OF_VARIABLE_RANGE != 0:
            return -2

        if round(new_range[1] / RESOLUTION_OF_VARIABLE_RANGE) - new_range[1] / RESOLUTION_OF_VARIABLE_RANGE != 0:
            return -2

        [io_variable, io_idx] = self._find_variable(io_variable_name, input_or_output)
        if input_or_output == "input":
            self._fis.Inputs.pop(io_idx)
            io_variable.Range = new_range
            self._fis.Inputs.insert(io_idx, io_variable)
        else:
            self._fis.Outputs.pop(io_idx)
            io_variable.Range = new_range
            self._fis.Outputs.insert(io_idx, io_variable)
        return 1

    def get_current_inference_type(self) -> fl.mamfis | fl.sugfis:
        """Get the type of inference system currently in use."""
        return type(self._fis)

    def convert_inference_system(self, new_fis_name: str) -> Self:
        """Converts fis to the other type of inference system.

        Args:
            new_fis_name (str): Name for the new fis.

        Returns:
            Self: New instance of FISModel class, with converted inference system.
        """
        if type(self._fis) is fl.mamfis:
            new_fis_model = FISModel(fis_type="sugeno", fis_name=new_fis_name, int_points=self._interpolation_points_nr)
            new_fis_model._fis.Inputs = self._fis.Inputs
            new_fis_model._fis.Outputs = self._fis.Outputs

            for output in new_fis_model._fis.Outputs:
                for mf in output.MembershipFunctions:
                    old_params = mf.Parameters
                    if isinstance(old_params, list) and len(old_params) > 0:
                        avg_value = sum(old_params) / len(old_params)
                    else:
                        avg_value = 0.5
                    mf.Type = "constant"
                    mf.Parameters = avg_value

            new_fis_model._fis.Rules = self._fis.Rules
            for rule in new_fis_model._fis.Rules:
                for idx in range(len(rule.IsMFOutput)):
                    if rule.IsMFOutput[idx] != 1:
                        rule.IsMFOutput[idx] = 1

            new_fis_model._fis.AndMethod = "prod"
            new_fis_model._fis.OrMethod = "probor"
            new_fis_model._fis.ImplicationMethod = "prod"
            new_fis_model._fis.AggregationMethod = "sum"
            new_fis_model._fis.DefuzzificationMethod = "wtaver"
            return new_fis_model

        if type(self._fis) is fl.sugfis:
            new_fis_model = FISModel(
                fis_type="mamdani", fis_name=new_fis_name, int_points=self._interpolation_points_nr
            )
            new_fis_model._fis.Inputs = self._fis.Inputs
            new_fis_model._fis.Outputs = self._fis.Outputs

            for output in new_fis_model._fis.Outputs:
                for mf in output.MembershipFunctions:
                    old_params = mf.Parameters
                    if isinstance(old_params, (int, float)):
                        center_value = old_params
                    elif isinstance(old_params, list) and len(old_params) > 0:
                        center_value = sum(old_params) / len(old_params)
                    else:
                        center_value = 0.5

                    mf.Type = "trimf"
                    output_range = output.Range
                    range_min = output_range[0] if output_range else 0
                    range_max = output_range[1] if output_range else 1
                    mf.Parameters = [
                        max(range_min, center_value - 0.4),
                        center_value,
                        min(range_max, center_value + 0.4),
                    ]

            new_fis_model._fis.Rules = self._fis.Rules

            new_fis_model._fis.AndMethod = "min"
            new_fis_model._fis.OrMethod = "max"
            new_fis_model._fis.ImplicationMethod = "min"
            new_fis_model._fis.AggregationMethod = "max"
            new_fis_model._fis.DefuzzificationMethod = "centroid"
            return new_fis_model

    def generate_all_rules(self) -> int:
        """Generate all possible rules, based on current input/output/mf configuration.

        If some rules are already present, generate only the missing ones.

        To stay compatible with Fuzzy Logic Designer, this function does not
        generate rules with input mfs being null. Also, it does not override
        such rules if they were added manually, instead appending a new, full
        rule.

        Returns:
            int: 1 if rules added successfully, -1 if there are no outputs and/or inputs,
                rules can't be generated, -2 if one or more variables do not have mfs defined,
                rules can't be generated.
        """
        if len(self._fis.Outputs) == 0 or len(self._fis.Inputs) == 0:
            return -1

        if not self._check_if_every_variable_has_mf():
            return -2

        output_mfs = [1 for _ in range(len(self._fis.Outputs))]
        mfs_per_input = []
        for input_nr in range(len(self._fis.Inputs)):
            mfs_per_input.append([])
            for mf_nr in range(1, len(self._fis.Inputs[input_nr].MembershipFunctions) + 1):
                mfs_per_input[input_nr].append(mf_nr)

        rule_combinations_tuple = list(itertools.product(*mfs_per_input))
        rule_combinations = [list(tup) for tup in rule_combinations_tuple]

        rules_input_part = [rule.Antecedent for rule in self._fis.Rules]
        for potential_rule in rule_combinations:
            if potential_rule not in rules_input_part:
                potential_rule_ext = [*potential_rule, *output_mfs, 1, 1]
                self.add_rule(None, potential_rule_ext)

        return 1

    def return_all_rules(self) -> list[FisRuleEx]:
        """Return a list if all available rules."""
        return self._fis.Rules

    def clear_all_io_variables(self) -> None:
        """Delete all input/output variables from the system."""
        self._fis.Inputs.clear()
        self._fis.Outputs.clear()
        self.clear_all_rules()

    def return_all_input_variables(self) -> list[fl.fisvar]:
        """Get all input variables of the system.

        Returns:
            A list (potentially empty) of all input variables of the system.
        """
        return self._fis.Inputs

    def return_all_output_variables(self) -> list[fl.fisvar]:
        """Get all output variables of the system.

        Returns:
            A list (potentially empty) of all output variables of the system.
        """
        return self._fis.Outputs

    def return_all_mfs_of_io_variable(self, io_variable_name: str, io_variable_type: str) -> list[fl.fismf] | None:
        """Get all membership functions of an input/output variable.

        Args:
            io_variable_name (str): name of the input/output variable whose mfs
                are to be returned
            io_variable_type (str): whether it is an input or output variable.
                Accepted values: input, output

        Returns:
            None, if a variable of the given type with the given name does not
                exist. A list (potentially empty) of all its membership
                functions otherwise.
        """
        if io_variable_type == "input":
            for input_variable in self._fis.Inputs:
                if input_variable.Name == io_variable_name:
                    return input_variable.MembershipFunctions
        if io_variable_type == "output":
            for output_variable in self._fis.Outputs:
                if output_variable.Name == io_variable_name:
                    return output_variable.MembershipFunctions

        return None

    def return_system_name(self) -> str:
        """Return the name of the Fuzzy Inference System used.

        Returns:
            The name (str) of the system.
        """
        return self._fis.Name

    def _find_variable(self, io_variable_name: str, input_or_output: str) -> [fl.fisvar, int]:
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

    def _find_available_element_number(self, element_type: str, io_variable: fl.fisvar = None) -> int:
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

    def _check_if_new_mf_type_is_valid(self, input_or_output: str, mf_type: str) -> [bool, str, list | int]:
        if type(self._fis) is fl.mamfis:
            if mf_type not in MF_TYPE_TO_FUNCTION_NAME.keys():
                return [False, "", -1]
            return [True, MF_TYPE_TO_FUNCTION_NAME[mf_type], DEFAULT_MF_PARAMS[mf_type]]

        if type(self._fis) is fl.sugfis:
            if input_or_output == "input":
                if mf_type not in MF_TYPE_TO_FUNCTION_NAME.keys():
                    return [False, "", -1]
                return [
                    True,
                    MF_TYPE_TO_FUNCTION_NAME[mf_type],
                    DEFAULT_MF_PARAMS[mf_type],
                ]
            if input_or_output == "output":
                if mf_type not in MF_TYPE_TO_FUNCTION_NAME_SUGENO.keys():
                    return [False, "", -1]
                return [
                    True,
                    MF_TYPE_TO_FUNCTION_NAME_SUGENO[mf_type],
                    DEFAULT_MF_PARAMS_SUGENO[mf_type],
                ]

    def _check_if_is_behaviour_list_is_valid(self, is_mf: list[int]) -> bool:
        if type(self._fis) is fl.sugfis:
            check_if_correct_for_sugeno = is_mf[len(self._fis.Inputs) :]
            if check_if_correct_for_sugeno.count(1) != len(check_if_correct_for_sugeno):
                return False

        return True
