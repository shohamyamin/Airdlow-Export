# Airflow User and Connection Export/Import

## Overview
This project provides a solution for exporting and importing Airflow users and connections. Airflow is an open-source platform used for orchestrating and scheduling complex workflows. However, the default functionality of Airflow does not provide a straightforward way to migrate users and connections between instances. This project aims to simplify this process by introducing export and import functionality.

## Features
- Export Airflow users and Connections: Export all users and Connections from one Airflow instance to a file, which can be used for importing into another instance.
- Import Airflow users and Connections: Import users and Connections from an exported file into an Airflow instance, allowing seamless migration of user accounts.

## Installation
1. Clone the repository: `git clone https://github.com/shohamyamin/Airdlow-Export.git`
2. Navigate to the project directory: `cd Airdlow-Export`
3. Navigate to the desired mode(Docker or Kubernetes) by: `cd docker` or `cd kubernetes`

## Configure from which Airflow instances to export
The way we export and import the users and the connections is from the CLI on the container itself.
To manage several airflow instances we configure a JSON file called `clients_objects.json`.
In this file, we configure from which pod and container we need to export and import the data.

The structure of the file is an array of airflow instances and each object represents one airflow instance:

`[
  {
    "client_pod_name": "airflow_client1_webserver_pod_name",
    "client_container_name": "airflow_client1_webserver_container_name",
    "client_name": "client1"
  },
  {
    "client_pod_name": "airflow_client2_webserver_pod_name",
    "client_container_name": "airflow_client2_webserver_container_name",
    "client_name": "client2"
  }
]`

- For getting all pods run: `kubectl get pods`
- For getting all containers in a specific pod run: `kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].name}'`

Please update this file according to your pods and containers
## Usage

### Export Users & Connections
1. Run the following command to export the users and the connections:

`python .\connection_users_export.py`

This will export all users and connections from the Airflow instance to a JSON file named `{client_name}_airflow_data.json` inside exports_files directory.


### Import Users & Connections
1. Ensure you have the `{client_name}_airflow_data.json` inside exports_files directory.
2. Run the following command to import users & connections into a new Airflow instance:

`python .\connection_users_import.py`

This will import the users & connections from the `{client_name}_airflow_data.json` file into the Airflow instance.

## Limitations
- This project currently supports exporting and importing users and connections in JSON format only.
- The import functionality assumes that the Airflow instance is set up and properly configured before running the import script.
- After importing the users need to reset the password

## Contributing
Contributions are welcome! If you encounter any issues or have ideas for improvements, please submit an issue or create a pull request on the project's GitHub repository.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
