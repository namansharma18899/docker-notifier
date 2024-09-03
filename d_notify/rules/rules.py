from abc import ABC, abstractmethod
from constants.enums import CState
from d_notify.alerts.rule_alert_handler import EmailNotification, SlackNotification, SystemNotification

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

class RuleEventHandler:
    def __init__(self, rule, event_handler) -> None:
        self.rule = {}

class RuleEngine:
    def __init__(self):
        self.rule_event_handler = {}

    def add_rule(self, rule, notification_handler):
        if rule.container_name not in self.rule_event_handler:
            self.rule_event_handler[rule.container_name] = {}
        # self.rules[rule.container_name].append(rule)
        # self.rule_event_handler[rule.container_name].append(RuleEventHandler(rule=rule, event_handler=notification_handler))
        self.rule_event_handler[rule.container_name][rule.name] = notification_handler

    def remove_rule(self, container_name, rule_type):
        if container_name in self.rule_event_handler.keys():
            self.rule_event_handler[container_name] = [
                reh for reh in self.rule_event_handler[container_name]
                if not isinstance(reh['rule'], rule_type)
            ]
            if not self.rule_event_handler[container_name]:
                del self.rule_event_handler[container_name]

    def evaluate_rules(self, container_info):
        container_name = container_info["name"]
        if container_name in self.rule_event_handler:
            for rule in self.rule_event_handler[container_name]['rule']:
                if not rule.evaluate(container_info):
                    return False
        return True

    def evaluate_rules_and_handle_notification(self, container_info):
        if self.evaluate_rules(container_info):
            self.rule_event_handler

# Example usge
if __name__=='__main__':
    rule_engine = RuleEngine()
    slack_notify = SlackNotification()
    system_notify = SystemNotification()
    rule_engine.add_rule(ContainerStateRule("nginx", CState.RUNNING.value), notification_handler=SystemNotification)
    rule_engine.add_rule(ResourceUtilizationRule(container_name="nginx", cpu_threshold=80, memory_threshold=500), notification_handler=SystemNotification)
    # rule_engine.add_rule(LogBasedRule(container_name="nginx", log_pattern="ERROR"))

    container_info = {
        "name": "nginx",
        "state": CState.RUNNING.value,
        "cpu_usage": 70,
        "memory_usage": 400,
        "logs": "INFO: Server started"
    }
    print(rule_engine.evaluate_rules(container_info))
