import os
import paramiko
from getpass import getpass
from dotenv import load_dotenv
from exceptions import ConnectionError, AuthenticationError, KeyNotFoundError, \
                      CommandExecutionError, KeyManagementError

class SSHConnection:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('SSH_HOST')
        self.port = int(os.getenv('SSH_PORT', 22))
        self.username = os.getenv('SSH_USERNAME')
        self.password = os.getenv('SSH_PASSWORD')
        self.key_path = os.getenv('SSH_KEY_PATH')
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            if self.key_path:
                self._connect_with_key()
            else:
                self._connect_with_password()
        except paramiko.SSHException as e:
            raise ConnectionError(f"SSH connection failed: {e}")
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}")

    def _connect_with_password(self):
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
        except paramiko.AuthenticationException as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}")

    def _connect_with_key(self):
        try:
            key = paramiko.RSAKey.from_private_key_file(self.key_path)
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                pkey=key
            )
        except paramiko.AuthenticationException as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except FileNotFoundError as e:
            raise KeyNotFoundError(f"Key file not found: {e}")
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}")

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            if error:
                raise CommandExecutionError(f"Command execution error: {error}")
            return output
        except paramiko.SSHException as e:
            raise ConnectionError(f"SSH connection error: {e}")
        except Exception as e:
            raise CommandExecutionError(f"Command execution error: {e}")

    def disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            raise ConnectionError(f"Error disconnecting: {e}")

    def manage_keys(self, action, key_path=None):
        if action == 'view':
            return self._view_key()
        elif action == 'edit' and key_path:
            return self._edit_key(key_path)
        else:
            raise ValueError("Invalid action or missing key path for edit.")

    def _view_key(self):
        try:
            if self.key_path and os.path.isfile(self.key_path):
                with open(self.key_path, 'r') as key_file:
                    return key_file.read()
            else:
                raise KeyNotFoundError("Key file not found.")
        except FileNotFoundError as e:
            raise KeyNotFoundError(f"Key file not found: {e}")
        except Exception as e:
            raise KeyManagementError(f"Error viewing key: {e}")

    def _edit_key(self, new_key_path):
        try:
            if os.path.isfile(new_key_path):
                self.key_path = new_key_path
                os.environ['SSH_KEY_PATH'] = self.key_path
                return "Key path updated successfully."
            else:
                raise KeyNotFoundError("New key file not found.")
        except FileNotFoundError as e:
            raise KeyNotFoundError(f"New key file not found: {e}")
        except Exception as e:
            raise KeyManagementError(f"Error editing key: {e}")

# Example usage
# if __name__ == "__main__":
#     ssh_conn = SSHConnection()
#     try:
#         ssh_conn.connect()
#         output = ssh_conn.execute_command('ls -la')
#         print(output)
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         ssh_conn.disconnect()