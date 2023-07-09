import json
import subprocess

def import_airflow_connections_users(client_pod_name,client_container_name,client_name):

    # Load data from JSON file
    with open(f"./exports_files/{client_name}_airflow_data.json", "r") as file:
        data = json.load(file)

    # Export connections data to a local JSON file
    connections_data = data.get("connections")
    with open(f"./exports_files/{client_name}_connections.json", "w") as file:
        json.dump(connections_data, file)

    # Copy the connections file from the local machine to the container
    subprocess.run(["kubectl", "cp", f"./exports_files/{client_name}_connections.json", f"{client_pod_name}:/tmp/{client_name}_connections.json", "-c", client_container_name])

    # Import connections from the file in the container
    subprocess.run(["kubectl", "exec", client_pod_name, "-c", client_container_name, "airflow", "connections", "import", f"/tmp/{client_name}_connections.json"])

    # Export users data to a local JSON file
    users_data = data.get("users")
    with open(f"./exports_files/{client_name}_users.json", "w") as file:
        json.dump(users_data, file)

    # Copy the users file from the local machine to the container
    subprocess.run(["kubectl", "cp", f"./exports_files/{client_name}_users.json", f"{client_pod_name}:/tmp/{client_name}_users.json","-c", client_container_name])

    # Import users from the file in the container
    subprocess.run(["kubectl", "exec", client_pod_name, "-c", client_container_name, "airflow", "users", "import", f"/tmp/{client_name}_users.json"])

    print(f"{client_name} Airflow connections and users imported successfully.")

def import_all_client_connetions_and_users(clients_containers):
    for client in clients_containers:
        import_airflow_connections_users(client.client_pod_name,client.client_container_name,client.client_name)
    

# Load objects from a JSON file
def load_objects_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    objects = []
    for item in data:
        obj = ClientObject(item['client_pod_name'],item['client_container_name'], item['client_name'])
        objects.append(obj)
    
    return objects

class ClientObject:
    def __init__(self,client_pod_name, container_name, client_name):
        self.client_pod_name = client_pod_name
        self.client_container_name = container_name
        self.client_name = client_name

# Load objects from a JSON file
json_file_path = './clients_objects.json'
client_containers = load_objects_from_json(json_file_path)
import_all_client_connetions_and_users(client_containers)
