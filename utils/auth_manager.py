import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class AuthManager:
    """
    A class to manage authorized users and their roles in the bot.
    It provides methods to load, save, check authorization, and manage users.

    Public Attributes:
        path (Path): The path to the JSON file where authorized users are stored.

    Private Attributes:
        _users (dict[int, dict]): A dictionary where keys are user IDs and values are dictionaries with user details.
    """

    def __init__(self, path: Path = Path("authorized_users.json")):
        """
        Initialize the AuthManager with the path to the JSON file.

        Args:
            path (Path): The path to the JSON file where authorized users are stored.
                        Defaults to "authorized_users.json".
        """
        self.path = path
        self._users = self._load()

    def _load(self) -> dict[int, dict]:
        """
        Load authorized users from the JSON file.

        Returns:
            dict[int, dict]: A dictionary where keys are user IDs and values are dictionaries with user details.
        """
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                users_list = raw.get("users", [])
                return {int(u["id"]): u for u in users_list}
        return {}

    def _save(self) -> None:
        """
        Save the current state of authorized users to the JSON file.

        Returns:
            None
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {"users": list(self._users.values())}, f, ensure_ascii=False, indent=2
            )

    def reload(self) -> None:
        """Reload the users list from the JSON file."""
        self._users = self._load()

    def is_authorized(self, user_id: int) -> bool:
        """
        Check if a user is authorized.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        return user_id in self._users

    def is_admin(self, user_id: int) -> bool:
        """
        Check if a user is an admin.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._users.get(user_id, {}).get("role") == "admin"

    def add_user(
        self,
        user_id: int,
        added_by: Optional[int],
        full_name: str = "",
        role: str = "user",
        notes: str = "",
    ) -> bool:
        """
        Add a new user to the authorized users list.

        Args:
            user_id (int): The ID of the user to add.
            full_name (str): The full name of the user. Defaults to an empty string.
            role (str): The role of the user. Defaults to "user". Other roles can be "admin" or "viewer".
            added_by (Optional[int]): The ID of the user who is adding this user.
            notes (str): Additional notes about the user. Defaults to an empty string.

        Returns:
            bool: True if user was added, False if already exists.
        """

        if user_id in self._users:
            return False

        self._users[user_id] = {
            "id": user_id,
            "full_name": full_name,
            "role": role,
            "added_by": added_by,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "notes": notes,
        }

        self._save()
        return True

    def remove_user(self, user_id: int) -> bool:
        """
        Remove a user from the authorized users list.

        Args:
            user_id (int): The ID of the user to remove.

        Returns:
            bool: True if the user was removed successfully, False if the user does not exist.
        """
        if user_id in self._users:
            del self._users[user_id]
            self._save()
            return True
        return False

    def get_list_users(self) -> dict[int, dict]:
        """
        Return a list of all authorized users.

        Returns:
            dict[int, dict]: A dictionary where keys are user IDs and values are dictionaries with user details.
        """
        return self._users

    def get_role(self, user_id: int) -> str:
        """
        Get the role of a user.

        Args:
            user_id (int): The ID of the user whose role is to be retrieved.

        Returns:
            str: The role of the user, or "viewer" if the user is not found.
        """
        return self._users.get(user_id, {}).get("role", "viewer")
