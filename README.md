## PyENI Documentation

**PyENI** is a Python library designed to provide field and first-level support teams with an alternative monitoring interface for Ericsson Network Manager (ENM). It's specifically tailored for technicians and contractors working within a Mobile Network Operator (MNO).

**Features:**

* **SSH Connection:** Securely connects to ENM servers and network nodes using SSH.
* **Security:** Implements robust authentication mechanisms, including password and key-based authentication.
* **QoS Metrics Retrieval:** Retrieves key Quality of Service (QoS) metrics from network elements.
* **Interface Testing:** Allows for testing the functionality of network interfaces.
* **Alarms and Alerts:** Provides access to real-time alarms and alerts from the network.
* **Diagramming:** Visualizes network topology for easier understanding.
* **Logging Maintenance:** Records maintenance actions performed on sites, including descriptions and recommendations.

**Target Audience:**

* **Field Technicians:** Provides a user-friendly interface for monitoring and troubleshooting network issues.
* **Contractors:** Enables efficient network management and reporting for contracted services.
* **First-Level Support Teams:** Facilitates quick and accurate problem identification and resolution.

**Installation:**

```bash
pip install pyeni
```

**Usage:**

**1. Configuration:**

- Create a `.env` file in your project directory with the following environment variables:
    ```
    DEVICE_TYPE=cisco_ios  # Replace with your device type
    IP_ADDRESS=your_enm_server_ip
    PORT=22  # Default SSH port
    USERNAME=your_enm_username
    PASSWORD=your_enm_password
    ```

**2. Connecting to ENM:**

```python
from pyeni import SSHConnection

ssh_conn = SSHConnection()
try:
    ssh_conn.connect()
    # Your code to interact with the ENM server
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh_conn.disconnect()
```

**3. Executing Commands:**

```python
output = ssh_conn.execute_command('show version')
print(output)
```

**4. Retrieving Metrics:**

```python
from pyeni import metrics

# Example: Get RSRP values for a specific cell
rsrp_data = metrics.get_rsrp_values(cell_id="your_cell_id")
print(rsrp_data)
```

**5. Managing Alarms:**

```python
from pyeni import alerts

# Example: Get all active alarms
active_alarms = alerts.get_active_alarms()
print(active_alarms)
```

**6. Visualizing Network Topology:**

```python
from pyeni import visualiser

# Example: Generate a network diagram from ENM output
network_data = visualiser.extract_network_data(enm_output)
visualiser.draw_network_diagram(network_data)
```

**7. Logging Maintenance:**

```python
from pyeni import maintenance_logs

# Example: Log a maintenance action
maintenance_log = maintenance_logs.MaintenanceLog()
maintenance_log.add_entry(
    equipment_name="RBS 123",
    date=datetime.date(2023, 10, 26),
    description="Replaced faulty power supply",
    recommendations="Check power supply regularly",
)
```

**Example Script:**

```python
from pyeni import SSHConnection, metrics, alerts, visualiser, maintenance_logs
import datetime

# ... (Configure environment variables in .env file) ...

ssh_conn = SSHConnection()
try:
    ssh_conn.connect()

    # Retrieve QoS metrics
    rsrp_data = metrics.get_rsrp_values(cell_id="your_cell_id")
    print("RSRP Data:", rsrp_data)

    # Get active alarms
    active_alarms = alerts.get_active_alarms()
    print("Active Alarms:", active_alarms)

    # Generate a network diagram
    enm_output = ssh_conn.execute_command("show network-topology")
    network_data = visualiser.extract_network_data(enm_output)
    visualiser.draw_network_diagram(network_data)

    # Log a maintenance action
    maintenance_log = maintenance_logs.MaintenanceLog()
    maintenance_log.add_entry(
        equipment_name="RBS 123",
        date=datetime.date(2023, 10, 26),
        description="Replaced faulty power supply",
        recommendations="Check power supply regularly",
    )

except Exception as e:
    print(f"Error: {e}")
finally:
    ssh_conn.disconnect()
```

**Documentation Structure:**

- **`pyeni` package:**
    - **`ssh.py`:** Contains the `SSHConnection` class for managing SSH connections.
    - **`metrics.py`:** Provides functions for retrieving QoS metrics.
    - **`alerts.py`:** Handles alarm and alert management.
    - **`visualiser.py`:**  Provides tools for network visualization.
    - **`maintenance_logs.py`:**  Manages maintenance logs.
    - **`utils.py`:**  Contains utility functions.
    - **`exceptions.py`:**  Defines custom exceptions for error handling.
    - **`interface.py`:**  Provides functions for interface testing.
    - **`security.py`:**  Handles security-related operations.
    - **`sdir_parent.py`:**  Provides functions for interacting with the ENM's "sdir" command.
    - **`main.py`:**  Example script demonstrating usage.
    - **`setup.py`:**  Setup script for package installation.

**License:**

MIT License

**Contributing:**

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

**Contact:**

Mayibongwe Moyo
myboemoyo@gmail.com

**Disclaimer:**

This documentation is provided as a guide for using PyENI. The library is still under development, and features may change in future versions.
