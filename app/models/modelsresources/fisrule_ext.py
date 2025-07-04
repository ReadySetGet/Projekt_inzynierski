"""Extension of the 'fisrule' fuzzylab class

Classes:

    FisRuleEx: extension class
"""
import fuzzylab as fl


class FisRuleEx(fl.fisrule):
    """Extension class for the 'fisrule' fuzzylab class.

    Changes:

        - added support for IS NOT variable to mf mappings when inferring
    """

    IsMFInput: list[int]
    """Input variable to mf mappings when inferring (1 - use IS, else use 
    IS NOT)."""

    IsMFOutput: list[int]
    """Output variable to mf mappings when inferring (1 - use IS, else use 
    IS NOT)."""

    def __init__(self, is_mf: list[int], rule_def: list[list[int]], *varargin):
        """Initialize the extension class instance. Extends 'fisrule''s
        '__init__()' method.

        Parameters:

            is_mf (list[int]): list of variable to mf mapping behaviours when
                inferring (1 - use IS, else - use IS NOT)
            rule_def (list[list[int]]): list in a form of [r1, r2, ...], where
                r1, r2, ... are rules (lists) in the form of [imf1, imf2, imf3,
                ..., omf1, omf2, omf3, ... w, c], where:
                    imf1, imf2, imf3, ... - index of the mf to be used for
                        the input variable at a given list index
                    omf1, omf2, omf3, ... - index of the mf to be used for
                        the output variable at a given list index
                    w - weight of the rule

                    c - connector of variable conditions in the rule
                        (1 - use AND, else - use OR)
        """
        numInputs = varargin[0]

        super().__init__(self, rule_def, *varargin)
        self.IsMFInput = is_mf[:numInputs]
        self.IsMFOutput = is_mf[numInputs:]
