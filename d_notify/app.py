from threading import Thread
import docker
import time
import psutil
import subprocess
from plyer import notification
import time
import os
from constants.enums import CState
from prompt_handler import RuleEngineApp
from rules.rules import ContainerStateRule, ResourceUtilizationRule, RuleEngine
from services.conatiner_monitoring import CMonitor


# def get_running_containers(client):
#     return {container.id: container.name for container in client.containers.list()}

# def monitor_containers():
#     client = docker.from_env()
#     previous_containers = get_running_containers(client)
#     print("Monitoring Docker containers...")
#     try:
#         while True:
#             time.sleep(5)  # Polling interval
#             current_containers = get_running_containers(client)
#             added_containers = set(current_containers.keys()) - set(previous_containers.keys())
#             removed_containers = set(previous_containers.keys()) - set(current_containers.keys())
#             for container_id in added_containers:
#                 print(f"Container added: {current_containers[container_id]} (ID: {container_id})")
#                 notify(f'Contianer Started: {current_containers[container_id]}',' ')
#             for container_id in removed_containers:
#                 # print(f"Container removed: {previous_containers[container_id]} (ID: {container_id})")
#                 notify(f'Contianer Removed: {container_id}',' ')
#             previous_containers = current_containers

            
#     except KeyboardInterrupt:
#         print("Monitoring stopped.")

if __name__ == "__main__":
    rule_handler = RuleEngineApp()
    rule_handler.run()
    rule_engine = RuleEngine()
    rule_engine.add_rule(ContainerStateRule("nginx", CState.RUNNING.value))
    # rule_engine.add_rule(ResourceUtilizationRule(container_name="nginx", cpu_threshold=80, memory_threshold=500))
    monitor = CMonitor(rule_handler, rule_engine)
    thread = Thread(target=monitor.monitor_containers)
    thread.daemon = True
    thread.start()
