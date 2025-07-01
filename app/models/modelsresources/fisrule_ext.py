import fuzzylab as fl


class FisRuleEx(fl.fisrule):
    IsMFInput: list[int]  # 1 - uses 'is', else - uses 'is not'
    IsMFOutput: list[int]

    def __init__(self, is_mf: list[int], rule_def: list[int], *varargin):
        numInputs = varargin[0]

        super().__init__(self, rule_def, *varargin)
        self.IsMFInput = is_mf[:numInputs]
        self.IsMFOutput = is_mf[numInputs:]
