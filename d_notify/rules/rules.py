from abc import ABC, abstractmethod
from constants.enums import CState

class Rule(ABC):
    def __init__(self, container_name):
        self.container_name = container_name

    @abstractmethod
    def evaluate(self, container_info):
        pass

class ContainerStateRule(Rule):
    def __init__(self, container_name, required_state):
        super().__init__(container_name)
        self.required_state = required_state

    def evaluate(self, container_info):
        return container_info["state"] == self.required_state

class ResourceUtilizationRule(Rule):
    def __init__(self, container_name, cpu_threshold, memory_threshold):
        super().__init__(container_name)
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold

    def evaluate(self, container_info):
        cpu_usage = container_info["cpu_usage"]
        memory_usage = container_info["memory_usage"]
        return cpu_usage <= self.cpu_threshold and memory_usage <= self.memory_threshold

class LogBasedRule(Rule):
    def __init__(self, container_name, log_pattern, last_n_logs_to_tail=50):
        super().__init__(container_name)
        self.log_pattern = log_pattern

    def evaluate(self, container_info):
        logs = container_info["logs"]
        return self.log_pattern in logs

class RuleEngine:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule):
        if rule.container_name not in self.rules:
            self.rules[rule.container_name] = []
        self.rules[rule.container_name].append(rule)

    def remove_rule(self, container_name, rule_type):
        if container_name in self.rules:
            self.rules[container_name] = [
                rule for rule in self.rules[container_name]
                if not isinstance(rule, rule_type)
            ]
            if not self.rules[container_name]:
                del self.rules[container_name]

    def evaluate_rules(self, container_info):
        container_name = container_info["name"]
        if container_name in self.rules:
            for rule in self.rules[container_name]:
                if not rule.evaluate(container_info):
                    return False
        return True

# Example usge
if __name__=='__main__':
    rule_engine = RuleEngine()
    rule_engine.add_rule(ContainerStateRule("nginx", CState.RUNNING.value))
    rule_engine.add_rule(ResourceUtilizationRule(container_name="nginx", cpu_threshold=80, memory_threshold=500))
    # rule_engine.add_rule(LogBasedRule(container_name="nginx", log_pattern="ERROR"))

    container_info = {
        "name": "nginx",
        "state": CState.RUNNING.value,
        "cpu_usage": 70,
        "memory_usage": 400,
        "logs": "INFO: Server started"
    }
    print(rule_engine.evaluate_rules(container_info))
