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
    range_str = values[1].strip()
    range_str = range_str.replace("[", "").replace("]", "")
    range_values = [v.strip() for v in range_str.split() if v.strip()]
    if len(range_values) < 2:
        msg = f"Invalid range format for {in_or_out} {i + 1}: {values[1]}"
        raise ValueError(msg)
    range_low = float(range_values[0])
    range_high = float(range_values[1])
    if range_low >= range_high:
        msg = f"Range low must be less than high for {in_or_out} {i + 1}"
        raise ValueError(msg)

    values = get_line(fid).split("=")
    assert values[0] == "NumMFs", f"Number of MFs for {in_or_out} {i + 1} expected"
    num_mfs = int(values[1])

    next_fis_io = fisvar([range_low, range_high], Name=var_name)

    return next_fis_io, num_mfs


def get_next_mf(fid, i, j, in_or_out):
    """Read and return the next membership function definition."""
    line = get_line(fid)
    if not line or line[:2] != "MF":
        msg = f"Next MF for {in_or_out} {i + 1} expected, got: {line}"
        raise ValueError(msg)

    parts = line.split("=", 1)
    if len(parts) < 2:
        msg = f"Invalid MF format: {line}"
        raise ValueError(msg)

    mf_header = parts[0].strip()
    mf_index = int(mf_header[2:])
    if mf_index != j + 1:
        msg = f"Correct MF index for {in_or_out} {i + 1} expected, got {mf_index}"
        raise ValueError(msg)

    mf_def = parts[1].strip()
    mf_parts = mf_def.split(":", 1)
    if len(mf_parts) < 2:
        msg = f"Invalid MF definition format: {line}"
        raise ValueError(msg)

    mf_name = mf_parts[0].strip().strip("'\"")
    mf_type_and_params = mf_parts[1].strip()

    comma_pos = mf_type_and_params.find("',")
    if comma_pos == -1:
        msg = f"Invalid MF type/params format: {line}"
        raise ValueError(msg)

    mf_type = mf_type_and_params[:comma_pos].strip().strip("'\"")
    params_str = mf_type_and_params[comma_pos + 2 :].strip()

    params_str = params_str.replace("[", "").replace("]", "")
    param_values = [v.strip() for v in params_str.split() if v.strip()]

    mf_params = []
    for val in param_values:
        try:
            mf_params.append(float(val))
        except ValueError:
            continue

    if not mf_params:
        msg = f"No valid parameters found in MF definition: {line}"
        raise ValueError(msg)

    next_mf = fismf(mf_type, mf_params, Name=mf_name)

    return next_mf


def get_next_rule(fid, num_inputs):
    """Read the next rule definition and return a `FisRuleEx` instance."""
    line_ext = get_line(fid)
    sections = [val.strip() for val in re.split(r";", line_ext) if val.strip()]

    if len(sections) < 1:
        msg = f"Malformed rule definition: {line_ext!r}"
        raise ValueError(msg)

    rule_part = sections[0].strip()
    values = [val for val in re.split(r":|,|\(|\)| ", rule_part) if val]

    if len(values) < num_inputs + 3:
        msg = f"Rule definition too short: {line_ext!r}"
        raise ValueError(msg)

    for index in range(len(values) - 2):
        try:
            values[index] = int(values[index])
        except ValueError:
            msg = f"Invalid rule value at index {index}: {values[index]}"
            raise ValueError(msg)

    try:
        weight_token = float(values[-2])
        values[-2] = int(weight_token) if weight_token.is_integer() else weight_token
        values[-1] = int(values[-1])
    except (ValueError, IndexError) as e:
        msg = f"Invalid weight or connection in rule: {line_ext!r}"
        raise ValueError(msg) from e

    num_outputs = len(values) - num_inputs - 2

    if len(sections) >= 3:
        is_mf_part = sections[1].strip()
        values_is_mf = [int(val) for val in re.split(r":|,|\(|\)| ", is_mf_part) if val]
        if len(values_is_mf) != num_inputs + num_outputs:
            values_is_mf = [1] * (num_inputs + num_outputs)
        rule_name = sections[2].strip()
    elif len(sections) >= 2:
        is_mf_part = sections[1].strip()
        values_is_mf = [int(val) for val in re.split(r":|,|\(|\)| ", is_mf_part) if val]
        if len(values_is_mf) != num_inputs + num_outputs:
            values_is_mf = [1] * (num_inputs + num_outputs)
        rule_name = "Rule"
    else:
        values_is_mf = [1] * (num_inputs + num_outputs)
        rule_name = "Rule"

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
