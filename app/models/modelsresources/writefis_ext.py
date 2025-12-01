"""Utilities for serialising FIS definitions to `.fis` files."""

from __future__ import annotations

from typing import TextIO


def writeFIS(fis, filename: str = "filename.fis") -> None:  # noqa: N802 (external API name)
    """Serialise the provided FIS instance into the specified file."""
    with open_output_file(filename) as fid:
        write_system_section(fid, fis)
        write_input_sections(fid, fis)
        write_output_sections(fid, fis)
        write_rules_section(fid, fis)


def open_output_file(filename: str) -> TextIO:
    """Return a writable text stream for the given FIS filename."""
    if filename and not filename.endswith(".fis"):
        filename += ".fis"

    return open(filename, "w", encoding="utf-8")


def write_system_section(fid: TextIO, fis) -> None:
    """Write the `[System]` section describing global properties."""
    fid.write("[System]\n")
    fid.write(f"Name='{fis.Name}'\n")
    fid.write(f"Type='{fis.Type}'\n")
    fid.write("Version=2.0\n")
    fid.write(f"NumInputs={len(fis.Inputs)}\n")
    fid.write(f"NumOutputs={len(fis.Outputs)}\n")
    fid.write(f"NumRules={len(fis.Rules)}\n")
    fid.write(f"AndMethod='{fis.AndMethod}'\n")
    fid.write(f"OrMethod='{fis.OrMethod}'\n")
    fid.write(f"ImpMethod='{fis.ImplicationMethod}'\n")
    fid.write(f"AggMethod='{fis.AggregationMethod}'\n")
    fid.write(f"DefuzzMethod='{fis.DefuzzificationMethod}'\n")


def write_input_sections(fid: TextIO, fis) -> None:
    """Write all input variable definitions."""
    for index, fis_input in enumerate(fis.Inputs, start=1):
        num_mfs = len(fis_input.MembershipFunctions)
        fid.write(f"\n[Input{index}]\n")
        fid.write(f"Name='{fis_input.Name}'\n")
        fid.write(f"Range={str(fis_input.Range).replace(',', '')}\n")
        fid.write(f"NumMFs={num_mfs}\n")
        for mf_index, mf in enumerate(fis_input.MembershipFunctions, start=1):
            parameters = str(mf.Parameters).replace(",", "")
            line = "MF{}='{}':'{}',{}\n".format(mf_index, mf.Name, mf.Type, parameters)
            fid.write(line)


def write_output_sections(fid: TextIO, fis) -> None:
    """Write all output variable definitions."""
    for index, fis_output in enumerate(fis.Outputs, start=1):
        num_mfs = len(fis_output.MembershipFunctions)
        fid.write(f"\n[Output{index}]\n")
        fid.write(f"Name='{fis_output.Name}'\n")
        fid.write(f"Range={str(fis_output.Range).replace(',', '')}\n")
        fid.write(f"NumMFs={num_mfs}\n")
        for mf_index, mf in enumerate(fis_output.MembershipFunctions, start=1):
            parameters = str(mf.Parameters).replace(",", "")
            line = "MF{}='{}':'{}',{}\n".format(mf_index, mf.Name, mf.Type, parameters)
            fid.write(line)


def write_rules_section(fid: TextIO, fis) -> None:
    """Write the `[Rules]` section for the provided FIS."""
    num_inputs = len(fis.Inputs)
    num_outputs = len(fis.Outputs)

    fid.write("\n[Rules]\n")

    for rule in fis.Rules:
        antecedent = rule.Antecedent
        consequent = rule.Consequent
        weight = rule.Weight
        connection = rule.Connection
        is_mf_values = rule.IsMFInput + rule.IsMFOutput
        rule_name = rule.Name

        if num_inputs > 0:
            if is_mf_values[0] == 0:
                antecedent[0] = (-1)*antecedent[0]
            fid.write(f"{antecedent[0]}")
            for index in range(1, num_inputs):
                if is_mf_values[index] == 0:
                    antecedent[index] = (-1) * antecedent[index]
                fid.write(f" {antecedent[index]}")
        fid.write(", ")

        for index in range(num_outputs):
            fid.write(f"{consequent[index]} ")

        if isinstance(weight, int):
            weight_str = str(weight)
        else:
            weight_str = format(weight, ".4f")
        fid.write(f"({weight_str}) : ")

        fid.write(str(connection) + "\n")