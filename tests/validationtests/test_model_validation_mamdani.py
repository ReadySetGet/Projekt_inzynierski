import os
import unittest

import fuzzylab as fl

from app.models.fis_model import FISModel
from app.models.fis_reader_writer import FISReaderWriter


class ModelValidationMamdaniTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = None
        self.new_model = None
        self.back_model = None
        self.resources_dir = os.path.join(os.path.dirname(__file__), "resources")

    def test_model_validation(self) -> None:
        # Model creation
        self.model = FISModel(fis_type="mamdani")
        self.assertNotEqual(self.model, None, "No model created")
        self.assertEqual(type(self.model._fis), fl.mamfis, "Wrong model type created")

        # Adding io variables
        nr_inputs = len(self.model._fis.Inputs)
        self.assertEqual(nr_inputs, 0, "Model has inputs upon creation")
        self.model.add_input()
        self.assertEqual(len(self.model._fis.Inputs), 1, "Input not added")

        nr_outputs = len(self.model._fis.Outputs)
        self.assertEqual(nr_outputs, 0, "Model has outputs upon creation")
        self.model.add_output()
        self.assertEqual(len(self.model._fis.Outputs), 1, "Output not added")

        # Adding MFs to io variables
        nr_mfs = len(self.model._fis.Inputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 0, "Input has MFs upon creation")
        result = self.model.add_mf("input0", "input")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.model._fis.Inputs[0].MembershipFunctions),
            nr_mfs + 1,
            "MF not added to input",
        )

        nr_mfs = len(self.model._fis.Inputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 1, "Previous MF not added correctly")
        result = self.model.add_mf("input0", "input")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.model._fis.Inputs[0].MembershipFunctions),
            nr_mfs + 1,
            "MF not added to input",
        )

        nr_mfs = len(self.model._fis.Outputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 0, "Output has MFs upon creation")
        result = self.model.add_mf("output0", "output")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.model._fis.Outputs[0].MembershipFunctions),
            nr_mfs + 1,
            "MF not added to output",
        )

        nr_mfs = len(self.model._fis.Outputs[0].MembershipFunctions)
        self.assertEqual(nr_mfs, 1, "Previous MF not added correctly")
        result = self.model.add_mf("output0", "output")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.model._fis.Outputs[0].MembershipFunctions),
            nr_mfs + 1,
            "MF not added to output",
        )

        # Adding some more inputs and MFs
        nr_inputs = len(self.model._fis.Inputs)
        self.assertEqual(nr_inputs, 1, "Previous input not added correctly")
        self.model.add_input()
        self.assertEqual(len(self.model._fis.Inputs), 2, "Input not added")

        nr_mfs = len(self.model._fis.Inputs[1].MembershipFunctions)
        self.assertEqual(nr_mfs, 0, "Input has MFs upon creation")
        result = self.model.add_mf("input1", "input")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.model._fis.Inputs[1].MembershipFunctions),
            nr_mfs + 1,
            "MF not added to input",
        )

        # Changing different MF parameters
        result = self.model.change_mf_name("output0", "output", 0, "newname")
        self.assertEqual(result, 1, "Wrong result value")
        self.assertEqual(self.model._fis.Outputs[0].MembershipFunctions[0].Name, "newname", "Wrong name of MF")

        result = self.model.change_mf_parameters("input0", "input", 0, [1, 2, 3])
        self.assertEqual(result, 1, "Wrong result value")
        self.assertEqual(
            self.model._fis.Inputs[0].MembershipFunctions[0].Parameters, [1, 2, 3], "Wrong parameters of MF"
        )

        result = self.model.change_mf_type("input1", "input", 0, "gaussowska")
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            self.model._fis.Inputs[1].MembershipFunctions[0].Type,
            "gaussmf",
            "Wrong type of MF",
        )

        # Adding rules
        result = self.model.add_rule(is_mf=[1, 1, 0], rule_data=[1, 1, 1, 1, 1])
        self.assertEqual(result, 1, "Rule not added correctly")
        self.assertEqual(len(self.model._fis.Rules), 1, "Rule not added to fis")

        result = self.model.add_rule(is_mf=[1, 1, 1], rule_data=[2, 1, 2, 0.4, 0])
        self.assertEqual(result, 1, "Rule not added correctly")
        self.assertEqual(len(self.model._fis.Rules), 2, "Rule not added to fis")

        # Some additional operations a user might want to do before proceeding
        # to inferring
        result = self.model.change_variable_range("input0", "input", [-3, 8])
        self.assertEqual(self.model._fis.Inputs[0].Range, [-3, 8], "Range of input variable not changed")
        self.assertEqual(result, 1, "Wrong return value")

        result = self.model.update_logic_methods(and_method="prod")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.AndMethod, "prod", "And method not updated")

        result = self.model.update_logic_methods(agg_method="probor")
        self.assertEqual(result, 1, "Wrong return value")
        self.assertEqual(self.model._fis.AggregationMethod, "probor", "Aggregation method not updated")

        result = self.model.change_defuzzification_method("lom")
        self.assertEqual(self.model._fis.DefuzzificationMethod, "lom", "Defuzzification method not changed")
        self.assertEqual(result, 1, "Wrong return value")

        result = self.model.set_interpolation_points(50)
        self.assertEqual(result, 1, "Problems with return value")
        self.assertEqual(self.model._interpolation_points_nr, 50, "Interpolation points not set")

        # Generating all rules and updating some of them
        result = self.model.generate_all_rules()
        self.assertEqual(len(self.model._fis.Rules), 2, "Wrong nr of rules generated")
        self.assertEqual(result, 1, "Wrong result code returned")

        self.model.update_rule(1, [1, 1, 1], [1, 1, 1, 0.3, 1])
        self.assertEqual(self.model._fis.Rules[1].Weight, 0.3, "Rule weight not updated")

        self.model.update_rule(1, [1, 1, 1], [2, 1, 1, 1, 1])
        self.assertEqual(self.model._fis.Rules[1].Antecedent[0], 2, "Rule MF used not updated")

        # Converting to Sugeno model
        self.new_model = self.model.convert_inference_system("new_model")
        self.assertNotEqual(self.new_model, None, "Conversion failed")
        self.assertEqual(self.new_model._fis.Name, "new_model", "Wrong name")
        self.assertEqual(type(self.new_model._fis), fl.sugfis, "Wrong type of fis")
        for rule in self.new_model._fis.Rules:
            self.assertEqual(rule.IsMFOutput, [1], "Invalid IS NOT present")
        for mf in self.new_model._fis.Outputs[0].MembershipFunctions:
            self.assertEqual(mf.Parameters, 0.5, "Wrong parameter conversion")

        # Exporting model
        self.writer = FISReaderWriter(self.new_model)
        os.makedirs(self.resources_dir, exist_ok=True)
        model_path = os.path.join(self.resources_dir, "model.fis")
        result = self.writer.write_fis(model_path)
        self.assertEqual(result, 1, "Wrong return value")
        self.assertNotEqual(self.writer.model, None, "Model not exported")

        # Adding an additional output
        nr_outputs = len(self.new_model._fis.Outputs)
        self.assertEqual(nr_outputs, 1, "Problems with previously added output")
        self.new_model.add_output()
        self.assertEqual(len(self.new_model._fis.Outputs), 2, "Output not added")

        # Converting back to Mamdani model
        self.back_model = self.new_model.convert_inference_system("back_model")
        self.assertNotEqual(self.back_model, None, "Conversion failed")
        self.assertEqual(self.back_model._fis.Name, "back_model", "Wrong name")
        self.assertEqual(type(self.back_model._fis), fl.mamfis, "Wrong type of fis")

        # Deleting from the model
        nr_rules = len(self.back_model._fis.Rules)
        result = self.back_model.delete_rule(1)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.back_model._fis.Rules), nr_rules - 1, "Rule not deleted")

        self.back_model.clear_all_rules()
        self.assertEqual(len(self.back_model._fis.Rules), 0, "Not all rules deleted")

        nr_mfs = len(self.back_model._fis.Inputs[0].MembershipFunctions)
        result = self.back_model.delete_mf("input0", "input", 1)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.back_model._fis.Inputs[0].MembershipFunctions),
            nr_mfs - 1,
            "Input MF not deleted",
        )

        nr_mfs = len(self.back_model._fis.Outputs[0].MembershipFunctions)
        result = self.back_model.delete_mf("output0", "output", 0)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(
            len(self.back_model._fis.Outputs[0].MembershipFunctions),
            nr_mfs - 1,
            "Output MF not deleted",
        )

        nr_outputs = len(self.back_model._fis.Outputs)
        result = self.back_model.delete_output(0)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.back_model._fis.Outputs), nr_outputs - 1, "Output not deleted")

        nr_inputs = len(self.back_model._fis.Inputs)
        result = self.back_model.delete_input(1)
        self.assertEqual(result, 1, "Wrong result code")
        self.assertEqual(len(self.back_model._fis.Inputs), nr_inputs - 1, "Input not deleted")

        self.back_model.clear_all_io_variables()
        self.assertEqual(len(self.back_model._fis.Inputs), 0, "Not all inputs deleted")
        self.assertEqual(len(self.back_model._fis.Outputs), 0, "Not all outputs deleted")
        self.assertEqual(len(self.back_model._fis.Rules), 0, "Not all rules deleted")

        # Importing the previous model
        self.reader = FISReaderWriter()
        model_path = os.path.join(self.resources_dir, "model.fis")
        result = self.reader.read_fis(model_path)
        self.assertEqual(result, 1, "Wrong return value")
        self.assertNotEqual(self.reader.model, None, "Model not imported")
        self.new_model = self.reader.model

        # Checking correct model data fetching
        fis_type = self.new_model.get_current_inference_type()
        self.assertEqual(fis_type, fl.sugfis, "Wrong type returned")

        input_vars = self.new_model.return_all_input_variables()
        self.assertEqual(len(input_vars), 2, "Not all inputs returned")
        self.assertEqual(len(input_vars[0].MembershipFunctions), 2, "Inputs returned without mfs")
        self.assertEqual(len(input_vars[1].MembershipFunctions), 1, "Inputs returned without mfs")

        output_vars = self.new_model.return_all_output_variables()
        self.assertEqual(len(output_vars), 1, "Not all outputs returned")
        self.assertEqual(len(output_vars[0].MembershipFunctions), 2, "Outputs returned without mfs")

        input_mfs = self.new_model.return_all_mfs_of_io_variable("input0", "input")
        self.assertEqual(len(input_mfs), 2, "Not all mfs returned")

        rules = self.new_model.return_all_rules()
        self.assertEqual(len(rules), 2, "Wrong length of rule list")

        points = self.new_model.get_interpolation_points()
        self.assertEqual(points, 100, "Wrong number of interpolation points received")

        name = self.new_model.return_system_name()
        self.assertEqual(name, "new_model", "Wrong name returned")

    def tearDown(self) -> None:
        del self.model
        del self.new_model
        del self.back_model


if __name__ == "__main__":
    unittest.main()
