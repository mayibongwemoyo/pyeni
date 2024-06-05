# Custom exceptions

class ConnectionError(Exception):
    """Raised when an SSH connection fails."""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class KeyNotFoundError(Exception):
    """Raised when a key file is not found."""
    pass

class CommandExecutionError(Exception):
    """Raised when a command fails to execute on the remote server."""
    pass

class KeyManagementError(Exception):
    """Raised for errors related to key management operations."""
    pass