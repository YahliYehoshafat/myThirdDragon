from dataclasses import dataclass


@dataclass
class UserDetails:
    """
    Current user details.
    """
    user_id: str
    username: str 
    user_email: str
    user_password: str