class DockerContainerHistory:
    def __init__(self):
        self.container_history = {}

    def _current_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    def add_container(self, container_id, metadata):
        print(f'Adding Container {container_id}, metadata: {metadata}')
        if container_id in self.container_history:
            raise ValueError("Container ID already exists.")
        self.container_history[container_id] = {
            "status": "running",
            "metadata": metadata,
            "history": [(self._current_timestamp(), "created")]
        }

    def stop_container(self, container_id):
        if container_id not in self.container_history:
            raise ValueError("Container ID does not exist.")
        if self.container_history[container_id]["status"] == "stopped":
            raise ValueError("Container is already stopped.")
        self.container_history[container_id]["status"] = "stopped"
        self.container_history[container_id]["history"].append(
            (self._current_timestamp(), "stopped")
        )

    def start_container(self, container_id):
        if container_id not in self.container_history:
            raise ValueError("Container ID does not exist.")
        if self.container_history[container_id]["status"] == "running":
            raise ValueError("Container is already running.")
        self.container_history[container_id]["status"] = "running"
        self.container_history[container_id]["history"].append(
            (self._current_timestamp(), "started")
        )

    def get_container_history(self, container_id):
        if container_id not in self.container_history:
            raise ValueError("Container ID does not exist.")
        return self.container_history[container_id]["history"]

    def get_stopped_containers(self):
        return [
            container_id
            for container_id, data in self.container_history.items()
            if data["status"] == "stopped"
        ]

    def get_running_containers(self):
        return [
            container_id
            for container_id, data in self.container_history.items()
            if data["status"] == "running"
        ]

# Example usage
# tracker = DockerContainerHistory()
# tracker.add_container("container1", {"name": "nginx"})
# tracker.stop_container("container1")
# tracker.add_container("container2", {"name": "redis"})
# stopped_containers = tracker.get_stopped_containers()
# running_containers = tracker.get_running_containers()
# print(tracker.get_container_history(container_id='container1'))
