from pathlib import Path
from typing import List

from PyQt6.QtCore import pyqtSignal

from app.models.fis_model import FISModel
from app.models.fis_reader_writer import FISReaderWriter
from app.utils.paths import PROJECTS_DIR
from app.view_models.base_view_model import BaseViewModel


class BrowserFrameViewModel(BaseViewModel):
    """View model for the browser frame view."""

    system_browser_updated = pyqtSignal(list)
    design_browser_updated = pyqtSignal(list)
    system_item_selected = pyqtSignal(str, dict)
    design_item_selected = pyqtSignal(str, dict)
    design_projects_updated = pyqtSignal(list)
    project_switched = pyqtSignal(str)

    def __init__(self) -> None:
        """Initialize the BrowserFrameViewModel."""
        super().__init__()
        self._system_items = []
        self._design_items = []
        self._projects_dir = PROJECTS_DIR
        self._projects_dir.mkdir(exist_ok=True)
        self._current_project_name = None
        self._projects = []
        self._initialize_default_projects()

    @property
    def system_items(self) -> List[dict]:
        """Get the system browser items."""
        return self._system_items

    @property
    def design_items(self) -> List[dict]:
        """Get the design browser items."""
        return self._design_items

    def _update_browser_data(self) -> None:
        """Update the browser data from the model."""
        if not self.fuzzy_service:
            return

        self._system_items = self._get_system_items()
        self.system_browser_updated.emit(self._system_items)

        self._design_items = self._get_design_items()
        self.design_browser_updated.emit(self._design_items)

    def _get_system_items(self) -> List[dict]:
        """Get system items from the FIS model."""
        items = []

        if not self.fuzzy_service:
            return items

        input_variables = self.fuzzy_service.get_input_variables()
        for i, input_var in enumerate(input_variables):
            items.append(
                {
                    "type": "input",
                    "name": input_var.get("name", f"Input_{i}"),
                    "index": i,
                    "range": input_var.get("range", [0, 1]),
                    "mf_count": len(input_var.get("membership_functions", [])),
                    "membership_functions": input_var.get("membership_functions", []),
                }
            )

        output_variables = self.fuzzy_service.get_output_variables()
        for i, output_var in enumerate(output_variables):
            items.append(
                {
                    "type": "output",
                    "name": output_var.get("name", f"Output_{i}"),
                    "index": i,
                    "range": output_var.get("range", [0, 1]),
                    "mf_count": len(output_var.get("membership_functions", [])),
                    "membership_functions": output_var.get("membership_functions", []),
                }
            )

        rules = self.fuzzy_service.get_rules()
        for i, rule in enumerate(rules):
            items.append(
                {
                    "type": "rule",
                    "name": rule.get("name", f"Rule_{i+1}"),
                    "index": i,
                    "antecedent": rule.get("antecedent", []),
                    "consequent": rule.get("consequent", []),
                    "weight": rule.get("weight", 1.0),
                    "connection": rule.get("connection", 1),
                }
            )

        return items

    def _get_design_items(self) -> List[dict]:
        """Get design items from the FIS model."""
        items = []

        if not self.fuzzy_service:
            return items

        input_variables = self.fuzzy_service.get_input_variables()
        for input_var in input_variables:
            var_name = input_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "input")
            for i, mf in enumerate(mfs):
                items.append(
                    {
                        "type": "input_mf",
                        "variable_name": var_name,
                        "name": mf.get("name", f"MF_{i}"),
                        "index": i,
                        "mf_type": mf.get("type", "triangular"),
                        "parameters": mf.get("parameters", []),
                    }
                )

        output_variables = self.fuzzy_service.get_output_variables()
        for output_var in output_variables:
            var_name = output_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "output")
            for i, mf in enumerate(mfs):
                items.append(
                    {
                        "type": "output_mf",
                        "variable_name": var_name,
                        "name": mf.get("name", f"MF_{i}"),
                        "index": i,
                        "mf_type": mf.get("type", "triangular"),
                        "parameters": mf.get("parameters", []),
                    }
                )

        return items

    def select_system_item(self, item_name: str, item_data: dict) -> None:
        """Handle system item selection."""
        self.system_item_selected.emit(item_name, item_data)

    def select_design_item(self, item_name: str, item_data: dict) -> None:
        """Handle design item selection."""
        self.design_item_selected.emit(item_name, item_data)

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_browser_data()

    def refresh_browser(self) -> None:
        """Refresh the browser data."""
        self._update_browser_data()

    def load_default_project_if_empty(self) -> None:
        """Load the first available project if the current FIS is empty."""
        if not self.fuzzy_service:
            return

        has_inputs = self.fuzzy_service.get_input_count() > 0
        has_outputs = self.fuzzy_service.get_output_count() > 0

        if not has_inputs or not has_outputs:
            projects = self.get_projects()
            if projects:
                first_project = projects[0]
                project_name = first_project.get("name", "")
                if project_name:
                    self.load_project(project_name)

    def get_projects(self) -> List[dict]:
        """Get list of all saved projects."""
        projects = []
        if not self._projects_dir.exists():
            return projects

        for file_path in self._projects_dir.glob("*.fis"):
            project_name = file_path.stem
            file_size = file_path.stat().st_size
            modified_time = file_path.stat().st_mtime
            projects.append(
                {
                    "name": project_name,
                    "path": str(file_path),
                    "size": file_size,
                    "modified": modified_time,
                }
            )

        projects.sort(key=lambda x: x["modified"], reverse=True)
        self._projects = projects
        return projects

    def refresh_projects(self) -> None:
        """Refresh the projects list and emit signal."""
        projects = self.get_projects()
        self.design_projects_updated.emit(projects)

    def save_current_project(self, project_name: str) -> bool:
        """Save the current FIS model as a project."""
        if not self.fuzzy_service:
            return False

        if not project_name:
            return False

        if not project_name.endswith(".fis"):
            project_name = f"{project_name}.fis"

        file_path = self._projects_dir / project_name

        success = self.fuzzy_service.export_model(str(file_path))
        if success:
            self._current_project_name = project_name.replace(".fis", "")
            self.refresh_projects()
        return success

    def load_project(self, project_name: str) -> bool:
        """Load a project from the projects directory."""
        if not project_name:
            return False

        if not project_name.endswith(".fis"):
            project_name = f"{project_name}.fis"

        file_path = self._projects_dir / project_name

        if not file_path.exists():
            print(f"Project file not found: {file_path}")
            return False

        if not self.fuzzy_service:
            print("Fuzzy service not available")
            return False

        try:
            success = self.fuzzy_service.import_model(str(file_path))
            if success:
                self._current_project_name = project_name.replace(".fis", "")
                self.refresh_browser()
                self.refresh_projects()
                self.project_switched.emit(self._current_project_name)
                self.notify_data_changed.emit()
            else:
                print(f"Failed to import project: {project_name}")
            return success
        except Exception as e:
            print(f"Error loading project {project_name}: {e}")
            return False

    def delete_project(self, project_name: str) -> bool:
        """Delete a project file."""
        if not project_name:
            return False

        if not project_name.endswith(".fis"):
            project_name = f"{project_name}.fis"

        file_path = self._projects_dir / project_name

        if not file_path.exists():
            return False

        try:
            file_path.unlink()
            if self._current_project_name == project_name.replace(".fis", ""):
                self._current_project_name = None
            self.refresh_projects()
            return True
        except Exception:
            return False

    def rename_project(self, old_name: str, new_name: str) -> bool:
        """Rename a project file."""
        if not old_name or not new_name:
            return False

        if not old_name.endswith(".fis"):
            old_name = f"{old_name}.fis"
        if not new_name.endswith(".fis"):
            new_name = f"{new_name}.fis"

        old_path = self._projects_dir / old_name
        new_path = self._projects_dir / new_name

        if not old_path.exists() or new_path.exists():
            return False

        try:
            old_path.rename(new_path)
            if self._current_project_name == old_name.replace(".fis", ""):
                self._current_project_name = new_name.replace(".fis", "")
            self.refresh_projects()
            return True
        except Exception:
            return False

    def add_imported_project(self, source_file_path: str) -> bool:
        """Add an imported FIS file to the projects directory and set it as active.

        Args:
            source_file_path: Path to the imported FIS file.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not source_file_path:
            return False

        try:
            import shutil

            source_path = Path(source_file_path)
            if not source_path.exists():
                return False

            reader = FISReaderWriter()
            result = reader.read_fis(str(source_path))

            if result == 1 and reader.model and reader.model._fis:
                fis_name = reader.model._fis.Name
                if fis_name:
                    project_name = f"{fis_name}.fis"
                else:
                    project_name = source_path.name
            else:
                project_name = source_path.name

            dest_path = self._projects_dir / project_name
            counter = 1
            while dest_path.exists():
                stem = Path(project_name).stem
                project_name = f"{stem}_{counter}.fis"
                dest_path = self._projects_dir / project_name
                counter += 1

            shutil.copy2(source_path, dest_path)
            self.refresh_projects()

            project_name_without_ext = project_name.replace(".fis", "")
            if self.load_project(project_name_without_ext):
                self.refresh_projects()
                return True
            else:
                self.refresh_projects()
                return False
        except Exception as e:
            print(f"Error adding imported project: {e}")
            return False

    def create_new_project(self, project_name: str, fis_type: str) -> bool:
        """Create a new project file with default data.

        Args:
            project_name: Name for the new project (without .fis extension).
            fis_type: Type of FIS system ('mamdani' or 'sugeno').

        Returns:
            bool: True if successful, False otherwise.
        """
        if not project_name or not fis_type:
            return False

        if not project_name.endswith(".fis"):
            project_name = f"{project_name}.fis"

        project_path = self._projects_dir / project_name

        if project_path.exists():
            return False

        try:
            self._create_fis_file_with_data(project_path, fis_type.lower(), project_name.replace(".fis", ""))
            self.refresh_projects()

            project_name_without_ext = project_name.replace(".fis", "")
            if self.load_project(project_name_without_ext):
                self.refresh_projects()
                return True
            return False
        except Exception as e:
            print(f"Error creating new project: {e}")
            return False

    def duplicate_project(self, old_name: str, new_name: str) -> bool:
        """Duplicate a project file."""
        if not old_name or not new_name:
            return False

        if not old_name.endswith(".fis"):
            old_name = f"{old_name}.fis"
        if not new_name.endswith(".fis"):
            new_name = f"{new_name}.fis"

        old_path = self._projects_dir / old_name
        new_path = self._projects_dir / new_name

        if not old_path.exists() or new_path.exists():
            return False

        try:
            import shutil

            shutil.copy2(old_path, new_path)
            self.refresh_projects()
            return True
        except Exception:
            return False

    @property
    def current_project_name(self) -> str:
        """Get the current project name."""
        return self._current_project_name

    def _initialize_default_projects(self) -> None:
        """Initialize 3 default project files with data."""
        default_projects = [
            {"name": "Mamdani1", "type": "mamdani", "display_name": "Mamdani1"},
            {"name": "Sugeno1", "type": "sugeno", "display_name": "Sugeno1"},
            {"name": "Mamdani2", "type": "mamdani", "display_name": "Mamdani2"},
        ]

        for project in default_projects:
            project_file = self._projects_dir / f"{project['name']}.fis"
            if project_file.exists():
                project_file.unlink()
            self._create_fis_file_with_data(project_file, project["type"], project["display_name"])

    def _is_file_empty(self, file_path: Path) -> bool:
        """Check if a FIS file is empty (no inputs/outputs)."""
        try:
            from app.models.fis_model import FISModel
            from app.models.fis_reader_writer import FISReaderWriter

            temp_model = FISModel()
            reader = FISReaderWriter(temp_model)
            result = reader.read_fis(str(file_path))

            if result == 1 and temp_model._fis:
                num_inputs = len(temp_model._fis.Inputs) if temp_model._fis.Inputs else 0
                num_outputs = len(temp_model._fis.Outputs) if temp_model._fis.Outputs else 0
                return num_inputs == 0 or num_outputs == 0
        except Exception:
            pass
        return True

    def _create_fis_file_with_data(self, file_path: Path, fis_type: str, display_name: str = None) -> None:
        """Create a FIS file with default data (2 inputs, 1 output, MFs, rules)."""
        if display_name is None:
            display_name = file_path.stem

        if fis_type.lower() == "sugeno":
            model = FISModel(fis_type="sugeno", fis_name=display_name)
        else:
            model = FISModel(fis_type="mamdani", fis_name=display_name)

        self._populate_fis_with_data(model, fis_type)

        writer = FISReaderWriter(model)
        writer.write_fis(str(file_path))

    def _populate_fis_with_data(self, model: FISModel, fis_type: str) -> None:
        """Populate FIS model with 2 inputs, 1 output, MFs, and rules."""
        range_min, range_max = 0.0, 1.0

        model.add_input()
        if model._fis.Inputs:
            model._fis.Inputs[0].Name = "input1"
            model._fis.Inputs[0].Range = [range_min, range_max]

        model.add_input()
        if len(model._fis.Inputs) > 1:
            model._fis.Inputs[1].Name = "input2"
            model._fis.Inputs[1].Range = [range_min, range_max]

        for input_var in model._fis.Inputs:
            input_name = input_var.Name
            self._add_input_mfs(model, input_name, range_min, range_max)

        model.add_output()
        if model._fis.Outputs:
            model._fis.Outputs[0].Name = "output1"
            model._fis.Outputs[0].Range = [range_min, range_max]
            if fis_type.lower() == "sugeno":
                self._add_sugeno_output_mfs(model, "output1")
            else:
                self._add_mamdani_output_mfs(model, "output1", range_min, range_max)

        self._add_rules(model, fis_type)

    def _add_input_mfs(self, model: FISModel, input_name: str, range_min: float, range_max: float) -> None:
        """Add membership functions to an input variable."""
        mid = (range_min + range_max) / 2
        low_mid = (range_min + mid) / 2
        high_mid = (mid + range_max) / 2

        model.add_mf(input_name, "input", "trojkatna")
        if model._fis.Inputs:
            for input_var in model._fis.Inputs:
                if input_var.Name == input_name and input_var.MembershipFunctions:
                    input_var.MembershipFunctions[-1].Parameters = [range_min, range_min, low_mid]
                    input_var.MembershipFunctions[-1].Name = "low"

        model.add_mf(input_name, "input", "trojkatna")
        if model._fis.Inputs:
            for input_var in model._fis.Inputs:
                if input_var.Name == input_name and input_var.MembershipFunctions:
                    if len(input_var.MembershipFunctions) > 1:
                        input_var.MembershipFunctions[-1].Parameters = [low_mid, mid, high_mid]
                        input_var.MembershipFunctions[-1].Name = "medium"

        model.add_mf(input_name, "input", "trojkatna")
        if model._fis.Inputs:
            for input_var in model._fis.Inputs:
                if input_var.Name == input_name and input_var.MembershipFunctions:
                    if len(input_var.MembershipFunctions) > 2:
                        input_var.MembershipFunctions[-1].Parameters = [high_mid, range_max, range_max]
                        input_var.MembershipFunctions[-1].Name = "high"

    def _add_mamdani_output_mfs(self, model: FISModel, output_name: str, range_min: float, range_max: float) -> None:
        """Add membership functions to a Mamdani output variable."""
        mid = (range_min + range_max) / 2
        low_mid = (range_min + mid) / 2
        high_mid = (mid + range_max) / 2

        model.add_mf(output_name, "output", "trojkatna")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    output_var.MembershipFunctions[-1].Parameters = [range_min, range_min, low_mid]
                    output_var.MembershipFunctions[-1].Name = "low"

        model.add_mf(output_name, "output", "trojkatna")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    if len(output_var.MembershipFunctions) > 1:
                        output_var.MembershipFunctions[-1].Parameters = [low_mid, mid, high_mid]
                        output_var.MembershipFunctions[-1].Name = "medium"

        model.add_mf(output_name, "output", "trojkatna")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    if len(output_var.MembershipFunctions) > 2:
                        output_var.MembershipFunctions[-1].Parameters = [high_mid, range_max, range_max]
                        output_var.MembershipFunctions[-1].Name = "high"

    def _add_sugeno_output_mfs(self, model: FISModel, output_name: str) -> None:
        """Add membership functions to a Sugeno output variable."""
        model.add_mf(output_name, "output", "stala")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    output_var.MembershipFunctions[-1].Parameters = [0.25]
                    output_var.MembershipFunctions[-1].Name = "low"

        model.add_mf(output_name, "output", "stala")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    if len(output_var.MembershipFunctions) > 1:
                        output_var.MembershipFunctions[-1].Parameters = [0.5]
                        output_var.MembershipFunctions[-1].Name = "medium"

        model.add_mf(output_name, "output", "stala")
        if model._fis.Outputs:
            for output_var in model._fis.Outputs:
                if output_var.Name == output_name and output_var.MembershipFunctions:
                    if len(output_var.MembershipFunctions) > 2:
                        output_var.MembershipFunctions[-1].Parameters = [0.75]
                        output_var.MembershipFunctions[-1].Name = "high"

    def _add_rules(self, model: FISModel, fis_type: str) -> None:
        """Add rules to the FIS model."""
        is_mf = [1, 1, 1]

        rule1_data = [1, 1, 1, 1, 1]
        model.add_rule(is_mf=is_mf, rule_data=rule1_data)
        if model._fis.Rules:
            model._fis.Rules[-1].Name = "Rule1"

        rule2_data = [2, 2, 2, 1, 1]
        model.add_rule(is_mf=is_mf, rule_data=rule2_data)
        if model._fis.Rules:
            model._fis.Rules[-1].Name = "Rule2"

        rule3_data = [3, 3, 3, 1, 1]
        model.add_rule(is_mf=is_mf, rule_data=rule3_data)
        if model._fis.Rules:
            model._fis.Rules[-1].Name = "Rule3"
