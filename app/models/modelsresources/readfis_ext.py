"""Utilities for reading extended FIS definition files."""

import re

from fuzzylab import fismf, fisvar, mamfis, sugfis

from .fisrule_ext import FisRuleEx


def readfis(filename=""):
    """Parse a `.fis` specification file and return the resulting FIS object.

    Parameters
    ----------
    filename:
        Optional path to the input file. When no extension is provided the
        function appends `.fis`.

    Returns
    -------
    fuzzylab.FIS
        The constructed FIS instance.

    Raises
    ------
    ValueError
        Propagated when the file structure does not conform to the expected
        format.
    """
    try:
        with open_input_file(filename) as fid:
            fis, num_inputs, num_outputs, num_rules = init_fis_struct(fid)
            read_fis_inputs(fid, fis, num_inputs)
            read_fis_outputs(fid, fis, num_outputs)
            read_rules(fid, fis, num_inputs, num_rules)

        return fis

    except ValueError as exc:
        raise ValueError from exc


def open_input_file(filename):
    """Return an open text stream for the requested `.fis` file."""
    if filename and not filename.endswith(".fis"):
        filename += ".fis"

    return open(filename, "r", encoding="utf-8")


def init_fis_struct(fid):
    """Initialise the top-level FIS structure using the `[System]` section."""
    get_line(fid)
    values = get_line(fid).split("=")
    assert values[0] == "Name", "Name of FIS expected"
    fis_name = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "Type", "Type of FIS expected"
    fis_type = values[1][1:-1]

    values = get_line(fid).split("=")
    if values[0] == "Version":
        values = get_line(fid).split("=")

    assert values[0] == "NumInputs", "Number of inputs expected"
    num_inputs = int(values[1])

    values = get_line(fid).split("=")
    assert values[0] == "NumOutputs", "Number of oututs expected"
    num_outputs = int(values[1])

    values = get_line(fid).split("=")
    assert values[0] == "NumRules", "Number of rules expected"
    num_rules = int(values[1])

    values = get_line(fid).split("=")
    assert values[0] == "AndMethod", "And method  expected"
    and_method = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "OrMethod", "Or method expected"
    or_method = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "ImpMethod", "Implication method expected"
    imp_method = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "AggMethod", "Aggregation method expected"
    agg_method = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "DefuzzMethod", "Defuzzification method expected"
    defuzz_method = values[1][1:-1]

    if fis_type == "sugeno":
        fis = sugfis(fis_name)
    elif fis_type == "mamdani":
        fis = mamfis(fis_name)
    else:
        msg = f"Unsupported FIS type: {fis_type}"
        raise ValueError(msg)

    fis.AndMethod = and_method
    fis.OrMethod = or_method
    fis.ImplicationMethod = imp_method
    fis.AggregationMethod = agg_method
    fis.DefuzzificationMethod = defuzz_method

    return fis, num_inputs, num_outputs, num_rules


def read_fis_inputs(fid, fis, num_inputs):
    """Populate the FIS with the input variable definitions."""
    for i in range(num_inputs):
        next_fis_input, num_mfs = get_next_fis_io(fid, i, "input")
        fis.Inputs.append(next_fis_input)

        for j in range(num_mfs):
            next_mf = get_next_mf(fid, i, j, "input")
            fis.Inputs[i].MembershipFunctions.append(next_mf)


def read_fis_outputs(fid, fis, num_outputs):
    """Populate the FIS with the output variable definitions."""
    for i in range(num_outputs):
        next_fis_input, num_mfs = get_next_fis_io(fid, i, "output")
        fis.Outputs.append(next_fis_input)

        for j in range(num_mfs):
            next_mf = get_next_mf(fid, i, j, "output")
            fis.Outputs[i].MembershipFunctions.append(next_mf)


def read_rules(fid, fis, num_inputs, num_rules):
    """Read the `[Rules]` section and attach all parsed rules to the FIS."""
    get_line(fid)
    for _ in range(num_rules):
        next_rule = get_next_rule(fid, num_inputs)
        fis.Rules.append(next_rule)


def get_next_fis_io(fid, i, in_or_out):
    """Return the next input or output definition along with MF count."""
    values = get_line(fid).split("put")
    if in_or_out == "input":
        assert values[0] == "[In", "Next input expected"
    else:
        assert values[0] == "[Out", "Next output expected"
    io_index = int(values[1][:-1])
    assert io_index == i + 1, "Incorrect i/o index read"

    values = get_line(fid).split("=")
    assert values[0] == "Name", f"Name of {in_or_out} {i + 1} expected"
    var_name = values[1][1:-1]

    values = get_line(fid).split("=")
    assert values[0] == "Range", f"Range for {in_or_out} {i + 1} expected"
    range_values = values[1].split(" ")
    range_low = float(range_values[0][1:])
    range_high = float(range_values[1][:-1])
    assert range_low < range_high, f"Correct range for {in_or_out} {i + 1} expected"

    values = get_line(fid).split("=")
    assert values[0] == "NumMFs", f"Number of MFs for {in_or_out} {i + 1} expected"
    num_mfs = int(values[1])

    next_fis_io = fisvar([range_low, range_high], Name=var_name)

    return next_fis_io, num_mfs


def get_next_mf(fid, i, j, in_or_out):
    """Read and return the next membership function definition."""
    values = re.split(r"=|:|,|]|\[| ", get_line(fid))
    assert values[0][:2] == "MF", f"Next MF for {in_or_out} {i + 1} expected"
    mf_index = int(values[0][2:])
    assert mf_index == j + 1, f"Correct MF index for {in_or_out} {i + 1} expected"
    mf_name = values[1][1:-1]
    mf_type = values[2][1:-1]
    mf_params = [float(val) for val in values[4:-1]]

    next_mf = fismf(mf_type, mf_params, Name=mf_name)

    return next_mf


def get_next_rule(fid, num_inputs):
    """Read the next rule definition and return a `FisRuleEx` instance."""
    line_ext = get_line(fid)
    sections = [val for val in re.split(r";", line_ext) if val]
    if len(sections) < 3:
        msg = f"Malformed rule definition: {line_ext!r}"
        raise ValueError(msg)

    values_is_mf = [int(val) for val in re.split(r":|,|\(|\)| ", sections[1]) if val]
    rule_name = sections[2][1:]

    values = [val for val in re.split(r":|,|\(|\)| ", sections[0]) if val]
    for index in range(len(values) - 2):
        values[index] = int(values[index])

    weight_token = float(values[-2])
    values[-2] = int(weight_token) if weight_token.is_integer() else weight_token
    values[-1] = int(values[-1])

    next_rule = FisRuleEx(values_is_mf, rule_name, [values], num_inputs)

    return next_rule


def get_line(fid):
    """Return the next non-empty, non-comment line from the file."""
    while True:
        line = fid.readline()
        if not line:
            break
        line = line.strip()

        if not comment_or_empty(line):
            break

    return line


def comment_or_empty(line):
    """Return True when the provided line is empty or a comment marker."""
    return len(line) == 0 or line[0] in {"#", "%"}
