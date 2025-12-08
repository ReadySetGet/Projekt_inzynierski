"""Extension module for inferring functionalities provided in 'fuzzylab' library.

Changed functions:

    fuzzify_input
    eval_rules_mamdani
"""

import warnings

import numpy as np
from fuzzylab.defuzz import defuzz
from fuzzylab.evalmf import evalmf


def evalfis(fis, user_input, rule_firing=False, num_points=101):
    """Evaluate fuzzy inference system with given input."""
    if type(user_input) is not np.ndarray:
        user_input = np.asarray([user_input])

    if user_input.ndim == 1:
        user_input = np.asarray([user_input])

    m, n = user_input.shape
    num_inputs = len(fis.Inputs)

    if m == num_inputs and n is not num_inputs:
        user_input = user_input.transpose()

    output = np.zeros((len(user_input), len(fis.Outputs)))

    for i in range(len(user_input)):
        rule_input = fuzzify_input(fis, user_input[i])
        firing_strength = eval_firing_strength(fis, rule_input)

        if fis.Type == "mamdani":
            rule_output = eval_rules_mamdani(fis, firing_strength, num_points)
            fuzzy_output = aggregate_output_mamdani(fis, rule_output)
            output[i] = defuzzify_output_mamdani(fis, fuzzy_output)
        elif fis.Type == "sugeno":
            rule_output = eval_rules_sugeno(fis, firing_strength, user_input[i])
            fuzzy_output = aggregate_output_sugeno(fis, rule_output)
            output[i] = defuzzify_output_sugeno(fis, fuzzy_output)

    if output.shape == (1, 1):
        output = output[0, 0]

    if rule_firing:
        return output, firing_strength
    else:
        return output


def fuzzify_input(fis, user_input):
    """Fuzzify input values using membership functions."""
    num_rules = len(fis.Rules)
    num_inputs = len(fis.Inputs)
    rule_input = np.zeros((num_rules, num_inputs))

    for i in range(num_rules):
        antecedent = fis.Rules[i].Antecedent
        for j in range(num_inputs):
            crisp_x = user_input[j]

            mf_index = antecedent[j] - 1
            mf = fis.Inputs[j].MembershipFunctions[mf_index]

            if fis.Rules[i].IsMFInput[j]:
                mu = evalmf(mf, crisp_x)
            else:
                mu = 1 - evalmf(mf, crisp_x)

            rule_input[i, j] = mu

    return rule_input


def eval_firing_strength(fis, rule_input):
    """Evaluate firing strength for each rule."""
    num_rules = len(fis.Rules)
    num_inputs = len(fis.Inputs)
    firing_strength = np.zeros(num_rules)

    for i in range(num_rules):
        rule = fis.Rules[i]
        antecedent_mus = []
        for j in range(num_inputs):
            if rule.Antecedent[j] != 0:
                mu = rule_input[i, j]
                antecedent_mus.append(mu)

        if rule.Connection == 1:
            connect = fis.AndMethod
        else:
            connect = fis.OrMethod

        if connect == "min":
            firing_strength[i] = rule.Weight * np.min(antecedent_mus)
        elif connect == "max":
            firing_strength[i] = rule.Weight * np.max(antecedent_mus)
        elif connect == "prod":
            firing_strength[i] = rule.Weight * np.prod(antecedent_mus)
        elif connect == "sum":
            firing_strength[i] = rule.Weight * np.sum(antecedent_mus)
        elif connect == "algebraic_product":
            firing_strength[i] = rule.Weight * np.prod(antecedent_mus)

    return firing_strength


def eval_rules_mamdani(fis, firing_strength, num_points):
    """Evaluate rules for Mamdani type fuzzy inference system."""
    num_rules = len(fis.Rules)
    num_outputs = len(fis.Outputs)
    rule_output = np.zeros((num_points, num_rules * num_outputs))

    for i in range(num_rules):
        rule = fis.Rules[i]
        rule_matching_degree = firing_strength[i]

        if rule_matching_degree != 0:
            for j in range(num_outputs):
                mf_index = rule.Consequent[j] - 1
                out_range = fis.Outputs[j].Range
                mf = fis.Outputs[j].MembershipFunctions[mf_index]
                x = np.linspace(out_range[0], out_range[1], num_points)

                if fis.Rules[i].IsMFOutput[j]:
                    fuzzy_out = evalmf(mf, x)
                else:
                    fuzzy_out = 1 - evalmf(mf, x)

                if fis.ImplicationMethod == "min":
                    fuzzy_out = np.minimum(rule_matching_degree, fuzzy_out)

                rule_output[:, (j - 1) * num_rules + i] = fuzzy_out

    return rule_output


def aggregate_output_mamdani(fis, rule_output):
    """Aggregate output for Mamdani type fuzzy inference system."""
    num_rules = len(fis.Rules)
    num_outputs = len(fis.Outputs)
    num_points = len(rule_output)
    fuzzy_output = np.zeros((num_points, num_outputs))

    for i in range(num_outputs):
        indiv_fuzzy_out = rule_output[:, i * num_rules : (i + 1) * num_rules]
        if fis.AggregationMethod == "max":
            agg_fuzzy_out = np.max(indiv_fuzzy_out, axis=1)
        fuzzy_output[:, i] = agg_fuzzy_out

    return fuzzy_output


def defuzzify_output_mamdani(fis, fuzzy_output):
    """Defuzzify output for Mamdani type fuzzy inference system."""
    num_outputs = len(fis.Outputs)
    num_points = len(fuzzy_output)
    output = np.zeros(num_outputs)

    for i in range(num_outputs):
        out_range = fis.Outputs[i].Range
        x = np.linspace(out_range[0], out_range[1], num_points)
        y = fuzzy_output[:, i]

        if np.all(y == 0):
            output[i] = (out_range[0] + out_range[1]) / 2.0
            continue

        max_y = np.max(y)
        if max_y == 0:
            output[i] = (out_range[0] + out_range[1]) / 2.0
            continue

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=RuntimeWarning, message=".*invalid value encountered in scalar divide.*"
            )
            try:
                result = defuzz(x, y, fis.DefuzzificationMethod)
                if np.isnan(result) or np.isinf(result):
                    output[i] = (out_range[0] + out_range[1]) / 2.0
                elif result < out_range[0] or result > out_range[1]:
                    result = np.clip(result, out_range[0], out_range[1])
                    output[i] = result
                else:
                    output[i] = result
            except (ValueError, ZeroDivisionError, Exception):
                output[i] = (out_range[0] + out_range[1]) / 2.0

    return output


def eval_rules_sugeno(fis, firing_strength, user_input):
    """Evaluate rules for Sugeno type fuzzy inference system."""
    num_rules = len(fis.Rules)
    num_outputs = len(fis.Outputs)
    rule_output = np.zeros((2, num_rules * num_outputs))

    for i in range(num_rules):
        rule = fis.Rules[i]
        rule_firing_strength = firing_strength[i]

        if rule_firing_strength != 0:
            for j in range(num_outputs):
                mf_index = rule.Consequent[j] - 1

                height = rule_firing_strength

                mf = fis.Outputs[j].MembershipFunctions[mf_index]

                if mf.Type == "constant":
                    if hasattr(mf.Parameters, "__getitem__"):
                        location = mf.Parameters[0]
                    else:
                        location = mf.Parameters
                elif mf.Type == "linear":
                    if hasattr(mf.Parameters, "__len__") and len(mf.Parameters) > len(user_input):
                        location = np.dot(mf.Parameters[:-1], user_input) + mf.Parameters[-1]
                    else:
                        if hasattr(mf.Parameters, "__getitem__"):
                            location = mf.Parameters[0]
                        else:
                            location = mf.Parameters

                rule_output[0, (j - 1) * num_rules + i] = location
                rule_output[1, (j - 1) * num_rules + i] = height

    return rule_output


def aggregate_output_sugeno(fis, rule_output):
    """Aggregate output for Sugeno type fuzzy inference system."""
    fuzzy_output = []
    num_outputs = len(fis.Outputs)
    num_rules = len(fis.Rules)

    for i in range(num_outputs):
        unagg_output = rule_output[:, i * num_rules : (i + 1) * num_rules]
        aggregated_output = aggregate_fis_output(fis.AggregationMethod, unagg_output)
        fuzzy_output.append(aggregated_output)

    return np.asarray(fuzzy_output)


def defuzzify_output_sugeno(fis, aggregated_output):
    """Defuzzify output for Sugeno type fuzzy inference system."""
    num_outputs = len(fis.Outputs)
    output = np.zeros(num_outputs)

    for i in range(num_outputs):
        next_agg_output = aggregated_output[i]
        x = next_agg_output[0]
        y = next_agg_output[1]

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=RuntimeWarning, message=".*invalid value encountered in scalar divide.*"
            )
            try:
                result = defuzz(x, y, fis.DefuzzificationMethod)
                if np.isnan(result) or np.isinf(result):
                    out_range = fis.Outputs[i].Range
                    output[i] = (out_range[0] + out_range[1]) / 2.0 if len(out_range) >= 2 else 0.0
                else:
                    output[i] = result
            except (ValueError, ZeroDivisionError):
                out_range = fis.Outputs[i].Range
                output[i] = (out_range[0] + out_range[1]) / 2.0 if len(out_range) >= 2 else 0.0

    return output


def aggregate_fis_output(fis_aggmethod, rule_output):
    """Aggregate FIS output based on the specified aggregation method."""
    rule_output = np.transpose(rule_output)
    mult_singletons = rule_output[rule_output[:, 0].argsort()]

    for i in range(len(mult_singletons) - 1):
        if mult_singletons[i, 0] == mult_singletons[i + 1, 0]:
            if fis_aggmethod == "sum":
                mult_singletons[i + 1, 1] = mult_singletons[i, 1] + mult_singletons[i + 1, 1]

            mult_singletons[i, 1] = 0

    mult_singletons = np.transpose(remove_null_rows(mult_singletons))

    return mult_singletons


def remove_null_rows(x):
    """Remove null rows from the input array."""
    y = []
    for i in range(len(x)):
        if x[i, 1] != 0:
            y.append(x[i])

    return np.asarray(y)
