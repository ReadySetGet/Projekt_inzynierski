"""Fuzzy Inference Engine for performing fuzzy calculations."""

from typing import Any, Dict, List, Optional, Tuple

from app.models.modelsresources.evalfis_ext import evalfis


class FuzzyInferenceEngine:
    """Engine for performing fuzzy inference calculations."""

    def __init__(self, fis_model) -> None:
        """Initialize the Fuzzy Inference Engine.

        Args:
            fis_model: The FIS model to perform calculations with.
        """
        self._fis_model = fis_model

    def perform_inference(self, inputs: List[float], fis_model: Optional[Any] = None) -> Tuple[List[float], bool]:
        """Perform fuzzy inference with given inputs.

        Args:
            inputs: List of input values for inference.
            fis_model: Optional FIS model to use (defaults to self._fis_model).

        Returns:
            Tuple of (output_values, success_flag).
        """
        try:
            if fis_model is None:
                fis_model = self._fis_model

            # Check if system is ready
            if not self._is_system_ready_for_inference(fis_model):
                return [], False

            # Perform inference using the evalfis function
            outputs = evalfis(fis_model._fis, inputs)

            if hasattr(outputs, "tolist"):
                outputs = outputs.tolist()
            elif not isinstance(outputs, list):
                outputs = [outputs] if not isinstance(outputs, (tuple, list)) else list(outputs)

            return outputs, True
        except Exception as e:
            print(f"Inference error: {e}")
            return [], False

    def batch_inference(
        self, input_batch: List[List[float]], fis_model: Optional[Any] = None
    ) -> List[Tuple[List[float], bool]]:
        """Perform batch fuzzy inference.

        Args:
            input_batch: List of input sets for batch inference.
            fis_model: Optional FIS model to use (defaults to self._fis_model).

        Returns:
            List of tuples containing (output_values, success_flag) for each input set.
        """
        results = []
        for inputs in input_batch:
            outputs, success = self.perform_inference(inputs, fis_model)
            results.append((outputs, success))
        return results

    def get_system_requirements(self, fis_model: Optional[Any] = None) -> Dict[str, Any]:
        """Get system requirements for inference.

        Args:
            fis_model: Optional FIS model to check (defaults to self._fis_model).

        Returns:
            Dictionary containing system requirements information.
        """
        if fis_model is None:
            fis_model = self._fis_model

        try:
            fis = fis_model._fis
            return {
                "input_count": len(fis.Inputs),
                "output_count": len(fis.Outputs),
                "rule_count": len(fis.Rules),
                "is_ready": self._is_system_ready_for_inference(fis_model),
                "input_ranges": [inp.Range for inp in fis.Inputs],
                "output_ranges": [out.Range for out in fis.Outputs],
            }
        except Exception:
            return {
                "input_count": 0,
                "output_count": 0,
                "rule_count": 0,
                "is_ready": False,
                "input_ranges": [],
                "output_ranges": [],
            }

    def validate_inputs(self, inputs: List[float], fis_model: Optional[Any] = None) -> Tuple[bool, str]:
        """Validate input values for inference.

        Args:
            inputs: List of input values to validate.
            fis_model: Optional FIS model to validate against (defaults to
                self._fis_model).

        Returns:
            Tuple of (is_valid, error_message).
        """
        try:
            if fis_model is None:
                fis_model = self._fis_model

            fis = fis_model._fis

            # Check if we have the right number of inputs
            if len(inputs) != len(fis.Inputs):
                return False, f"Expected {len(fis.Inputs)} inputs, got {len(inputs)}"

            # Check if inputs are within valid ranges
            for i, (input_val, input_var) in enumerate(zip(inputs, fis.Inputs)):
                if not isinstance(input_val, (int, float)):
                    return False, f"Input {i} must be a number, got {type(input_val)}"

                range_min, range_max = input_var.Range
                if not (range_min <= input_val <= range_max):
                    return (
                        False,
                        f"Input {i} ({input_val}) is outside range [{range_min},  {range_max}]",
                    )

            return True, ""
        except Exception as e:
            return False, f"Validation error: {e}"

    def get_inference_statistics(self, fis_model: Optional[Any] = None) -> Dict[str, Any]:
        """Get statistics about the inference system.

        Args:
            fis_model: Optional FIS model to analyze (defaults to self._fis_model).

        Returns:
            Dictionary containing inference statistics.
        """
        if fis_model is None:
            fis_model = self._fis_model

        try:
            fis = fis_model._fis

            # Count membership functions
            total_mfs = 0
            for inp in fis.Inputs:
                total_mfs += len(inp.MembershipFunctions)
            for out in fis.Outputs:
                total_mfs += len(out.MembershipFunctions)

            return {
                "total_inputs": len(fis.Inputs),
                "total_outputs": len(fis.Outputs),
                "total_rules": len(fis.Rules),
                "total_membership_functions": total_mfs,
                "average_mfs_per_input": total_mfs / len(fis.Inputs) if fis.Inputs else 0,
                "average_mfs_per_output": total_mfs / len(fis.Outputs) if fis.Outputs else 0,
                "system_complexity": len(fis.Rules) * total_mfs,
            }
        except Exception:
            return {
                "total_inputs": 0,
                "total_outputs": 0,
                "total_rules": 0,
                "total_membership_functions": 0,
                "average_mfs_per_input": 0,
                "average_mfs_per_output": 0,
                "system_complexity": 0,
            }

    def _is_system_ready_for_inference(self, fis_model: Optional[Any] = None) -> bool:
        """Check if the system is ready for inference.

        Args:
            fis_model: Optional FIS model to check (defaults to self._fis_model).

        Returns:
            True if system is ready, False otherwise.
        """
        try:
            if fis_model is None:
                fis_model = self._fis_model

            fis = fis_model._fis
            return len(fis.Inputs) > 0 and len(fis.Outputs) > 0 and len(fis.Rules) > 0
        except Exception:
            return False
