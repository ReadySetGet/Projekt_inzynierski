"""Rule Manager for managing FIS rules."""

from typing import Dict, List

from app.models.fis_model import FISModel


class RuleManager:
    """Manages FIS rules."""

    def __init__(self, fis_model: FISModel) -> None:
        """Initialize the Rule Manager.

        Args:
            fis_model: The FIS model to manage rules for.
        """
        self._fis_model = fis_model

    def get_rules(self) -> List[Dict[str, any]]:
        """Get all rules.

        Returns:
            List of dictionaries containing rule information.
        """
        rules = []
        try:
            for i, rule in enumerate(self._fis_model._fis.Rules):
                rule_data = {
                    "index": i,
                    "name": rule.Name,
                    "antecedent": rule.Antecedent.copy(),
                    "consequent": rule.Consequent.copy(),
                    "weight": rule.Weight,
                    "connection": rule.Connection,
                    "is_mf": rule.IsMF.copy() if hasattr(rule, "IsMF") else [],
                }
                rules.append(rule_data)
        except Exception:
            pass
        return rules

    def add_rule(
        self,
        antecedent: List[int],
        consequent: List[int],
        rule_name: str = "Rule",
        weight: float = 1.0,
        connection: int = 1,
        is_mf: List[int] = None,
    ) -> bool:
        """Add a new rule.

        Args:
            rule_name: Name of the rule.
            antecedent: Antecedent conditions.
            consequent: Consequent conditions.
            weight: Weight of the rule.
            connection: Connection type (1=AND, 0=OR).
            is_mf: IsMF flags for the rule.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if is_mf is None:
                is_mf = [1] * (len(antecedent) + len(consequent))

            result = self._fis_model.add_rule(
                is_mf,
                antecedent + consequent + [weight, connection],
            )
            if result == 1:
                if self._fis_model._fis.Rules:
                    self._fis_model._fis.Rules[-1].Name = rule_name
                return True
            return False
        except Exception:
            return False

    def delete_rule(self, rule_index: int) -> bool:
        """Delete a rule by index.

        Args:
            rule_index: Index of the rule to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.delete_rule(rule_index)
            return result == 1
        except Exception:
            return False

    def update_rule(
        self,
        rule_index: int,
        new_antecedent: List[int],
        new_consequent: List[int],
        new_weight: float,
        new_connection: int,
        new_is_mf: List[int],
    ) -> bool:
        """Update a rule.

        Args:
            rule_index: Index of the rule to update.
            new_antecedent: New antecedent conditions.
            new_consequent: New consequent conditions.
            new_weight: New weight of the rule.
            new_connection: New connection type (1=AND, 0=OR).
            new_is_mf: New IsMF flags for the rule.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            new_rule_data = new_antecedent + new_consequent + [new_weight, new_connection]
            result = self._fis_model.update_rule(rule_index, new_is_mf, new_rule_data)
            return result == 1
        except Exception:
            return False

    def update_rule_name(self, rule_index: int, new_name: str) -> bool:
        """Update the name of a rule.

        Args:
            rule_index: Index of the rule.
            new_name: New name for the rule.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= rule_index < len(self._fis_model._fis.Rules):
                self._fis_model._fis.Rules[rule_index].Name = new_name
                return True
            return False
        except Exception:
            return False

    def update_rule_weight(self, rule_index: int, new_weight: float) -> bool:
        """Update the weight of a rule.

        Args:
            rule_index: Index of the rule.
            new_weight: New weight for the rule.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= rule_index < len(self._fis_model._fis.Rules):
                self._fis_model._fis.Rules[rule_index].Weight = new_weight
                return True
            return False
        except Exception:
            return False

    def update_rule_connection(self, rule_index: int, new_connection: int) -> bool:
        """Update the connection type of a rule.

        Args:
            rule_index: Index of the rule.
            new_connection: New connection type (1=AND, 0=OR).

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= rule_index < len(self._fis_model._fis.Rules):
                self._fis_model._fis.Rules[rule_index].Connection = new_connection
                return True
            return False
        except Exception:
            return False

    def clear_all_rules(self) -> bool:
        """Clear all rules.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.clear_all_rules()
            return result == 1
        except Exception:
            return False

    def get_rule_text(self, rule_index: int) -> str:
        """Get the text representation of a rule.

        Args:
            rule_index: Index of the rule.

        Returns:
            String representation of the rule.
        """
        try:
            if not (0 <= rule_index < len(self._fis_model._fis.Rules)):
                return ""

            rule = self._fis_model._fis.Rules[rule_index]
            fis = self._fis_model._fis

            antecedent_parts = []
            for i, mf_idx in enumerate(rule.Antecedent):
                if mf_idx > 0:  # 0 means no condition
                    if i < len(fis.Inputs):
                        input_name = fis.Inputs[i].Name
                        if mf_idx <= len(fis.Inputs[i].MembershipFunctions):
                            mf_name = fis.Inputs[i].MembershipFunctions[mf_idx - 1].Name
                            is_not = "not " if (i < len(rule.IsMF) and rule.IsMF[i] != 1) else ""
                            antecedent_parts.append(f"{input_name} is {is_not}{mf_name}")

            consequent_parts = []
            for i, mf_idx in enumerate(rule.Consequent):
                if mf_idx > 0:  # 0 means no condition
                    if i < len(fis.Outputs):
                        output_name = fis.Outputs[i].Name
                        if mf_idx <= len(fis.Outputs[i].MembershipFunctions):
                            mf_name = fis.Outputs[i].MembershipFunctions[mf_idx - 1].Name
                            output_idx = i + len(rule.Antecedent)
                            is_not = "not " if (output_idx < len(rule.IsMF) and rule.IsMF[output_idx] != 1) else ""
                            consequent_parts.append(f"{output_name} is {is_not}{mf_name}")

            connection = " and " if rule.Connection == 1 else " or "
            antecedent_text = connection.join(antecedent_parts)
            consequent_text = " and ".join(consequent_parts)

            return f"If {antecedent_text} then {consequent_text} (weight: {rule.Weight})"
        except Exception:
            return ""

    def get_rule_count(self) -> int:
        """Get the number of rules.

        Returns:
            Number of rules.
        """
        try:
            return len(self._fis_model._fis.Rules)
        except Exception:
            return 0
