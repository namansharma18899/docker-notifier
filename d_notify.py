import docker
import time
import psutil
import subprocess
from plyer import notification
import time
import os

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Process Monitor",
        timeout=10  # Notification will stay for 10 seconds
    )


def get_running_containers(client):
    return {container.id: container.name for container in client.containers.list()}

def monitor_containers():
    client = docker.from_env()
    previous_containers = get_running_containers(client)
    print("Monitoring Docker containers...")
    try:
        while True:
            time.sleep(5)  # Polling interval
            current_containers = get_running_containers(client)
            added_containers = set(current_containers.keys()) - set(previous_containers.keys())
            removed_containers = set(previous_containers.keys()) - set(current_containers.keys())
            for container_id in added_containers:
                print(f"Container added: {current_containers[container_id]} (ID: {container_id})")
                notify(f'Contianer Started: {current_containers[container_id]}',' ')
            for container_id in removed_containers:
                # print(f"Container removed: {previous_containers[container_id]} (ID: {container_id})")
                notify(f'Contianer Removed: {container_id}',' ')
            previous_containers = current_containers

            
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    monitor_containers()

