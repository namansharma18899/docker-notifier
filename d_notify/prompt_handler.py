from enum import Enum
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from d_notify.services.conatiner_monitoring import CMonitor

class ContainerState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"
    RESTARTING = "restarting"
    EXITED = "exited"

class RuleEngineApp:
    def __init__(self):
        self.rules = []

    def run(self):
        self.show_main_menu()

    def show_main_menu(self):
        rule_type = inquirer.select(
            message="Select a rule to apply:",
            choices=[
                "Container State Rule",
                "Resource Utilization Rule",
                "Log Based Rule",
                Separator(),
                "Exit"
            ],
        ).execute()
        if rule_type == "Exit":
            print("Exiting the application.")
            return

        self.collect_rule_parameters(rule_type)
        # inquirer.confirm('Confirm --> ')
        print('Saving & Exiting...')
        return
        # self.show_main_menu()

    def collect_rule_parameters(self, rule_type):
        container_name = inquirer.text(
            message="Enter the container name:",
        ).execute()

        if rule_type == "Container State Rule":
            state = inquirer.select(
                message="Select the container state:",
                choices=[state.value for state in ContainerState],
            ).execute()
            self.rules.append({"type": rule_type, "container_name": container_name, "state": state})

        elif rule_type == "Resource Utilization Rule":
            cpu_threshold = inquirer.text(
                message="Enter the CPU usage threshold (%):",
                validate=lambda result: result.isdigit() and 0 <= int(result) <= 100,
            ).execute()
            memory_threshold = inquirer.text(
                message="Enter the memory usage threshold (MB):",
                validate=lambda result: result.isdigit() and int(result) > 0,
            ).execute()
            self.rules.append({
                "type": rule_type, "container_name": container_name,
                "cpu_threshold": cpu_threshold, "memory_threshold": memory_threshold
            })

        elif rule_type == "Log Based Rule":
            log_pattern = inquirer.text(
                message="Enter the log pattern to match:",
            ).execute()
            self.rules.append({"type": rule_type, "container_name": container_name, "log_pattern": log_pattern})

        print(f"Rule added: {self.rules[-1]}")
