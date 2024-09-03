import docker
import time
import psutil
import subprocess
from plyer import notification
import time
import os
from prompt_handler import RuleEngineApp
from rules.rules import RuleEngine
from services import notify
from services.container_history import DockerContainerHistory


class CMonitor:
    def __init__(self, rule_handler: RuleEngineApp, rule_engine: RuleEngine) -> None:
        self.rule_handler = rule_handler
        self.rule_engine = rule_engine
        self.polling_period_sec = 5 # seconds
        self.docker_history = DockerContainerHistory()
        self.client = docker.from_env()
        grc = self.get_running_containers(self.client)
        for c_id, c_mtd in grc.items():
            self.docker_history.add_container(container_id=c_id, metadata=c_mtd)
            self.previous_containers = grc

    def get_running_containers(self,client):
        return {container.id:{"name": container.name} for container in client.containers.list()}

    def monitor_containers(self):
        print("Monitoring Docker containers...")
        try:
            while True:
                time.sleep(self.polling_period_sec)  # Polling interval
                current_containers = self.get_running_containers(self.client)
                added_containers = set(current_containers.keys()) - set(self.previous_containers.keys())
                removed_containers = set(self.previous_containers.keys()) - set(current_containers.keys()) 
                for cid in added_containers:
                    self.docker_history.add_container(cid, current_containers[cid])
                for cid in removed_containers:
                    self.docker_history.stop_container(cid)
                # Hand it to NotificationHandler 
                # for container_id in added_containers:
                #     print(f"Container added: {current_containers[container_id]} (ID: {container_id})")
                #     notify(f'Contianer Started: {current_containers[container_id]}',' ')
                # for container_id in removed_containers:
                #     # print(f"Container removed: {previous_containers[container_id]} (ID: {container_id})")
                #     notify(f'Contianer Removed: {container_id}',' ')


                self.previous_containers = current_containers
        except KeyboardInterrupt:
            print("Monitoring stopped...")

# if __name__ == "__main__":
#     monitor_containers()