from security import Security
from ssh import SSHConnection
from .monitoring import Monitoring  # Example: Add your monitoring module

class pyeni:
    def __init__(self):
        load_dotenv()
        self.security = Security(os.getenv('PASSWORD_FILE_PATH'))
        self.ssh_conn = SSHConnection()
        self.monitoring = Monitoring()  # Example: Initialize monitoring module

    # ... (rest of the pyeni class code)