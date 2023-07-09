import json
import subprocess

def export_airflow_connections_users(client_pod_name,client_container_name,client_name):

    # Export connections to a file in the container
    subprocess.run(["kubectl", "exec",client_pod_name, "-c", client_container_name, "airflow", "connections", "export", f"/tmp/{client_name}_connections.json"])

    # Copy the connections file from the container to the local machine
    subprocess.run(["kubectl", "cp", f"{client_pod_name}:/tmp/{client_name}_connections.json", f"./exports_files/{client_name}_connections.json","-c", client_container_name])

    # Load connections from the local JSON file
    with open(f"./exports_files/{client_name}_connections.json", "r") as file:
        connections_data = json.load(file)

    # Export users to a file in the container
    subprocess.run(["kubectl", "exec", client_pod_name, "-c", client_container_name, "airflow", "users", "export","-v", f"/tmp/{client_name}_users.json"])

    # Copy the users file from the container to the local machine
    subprocess.run(["kubectl", "cp", f"{client_pod_name}:/tmp/{client_name}_users.json", f"./exports_files/{client_name}_users.json","-c",client_container_name])

    # Load users from the local JSON file
    with open(f"./exports_files/{client_name}_users.json", "r") as file:
        users_data = json.load(file)

    # Combine connections and users data
    data = {
        "connections": connections_data,
        "users": users_data
    }

    # Save data to JSON file
    with open(f"./exports_files/{client_name}_airflow_data.json", "w") as file:
        json.dump(data, file)

    print(f"{client_name} Airflow connections and users exported successfully.")

def export_all_client_connetions_and_users(clients_containers):
    for client in clients_containers:
        export_airflow_connections_users(client.client_pod_name,client.client_container_name,client.client_name)
    


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
export_all_client_connetions_and_users(client_containers)
