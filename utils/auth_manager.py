from datetime import datetime, timezone
from typing import Optional

from redis.asyncio import Redis


class AuthManager:
    """
    AuthManager class for managing user authorization and permissions.

    This class provides methods to add, remove, and check users and their roles using Redis as the storage backend.

    Attributes:
        redis (Redis): Redis client instance.
        prefix (str): Prefix for Redis keys.
    """

    def __init__(self, redis: Redis, prefix: str = "auth") -> None:
        """
        Initialize the AuthManager with a Redis client instance and a prefix for Redis keys.

        Args:
            redis (Redis): Redis client instance.
            prefix (str): Prefix for Redis keys. Defaults to "auth".
        """
        self.redis = redis
        self.prefix = prefix

    def _user_key(self, user_id: int) -> str:
        """
        Returns a Redis key for the given user ID.

        The key is constructed by concatenating the prefix, "user:", and the user ID.

        Args:
            user_id (int): User ID.

        Returns:
            str: Redis key for the given user ID.
        """
        return f"{self.prefix}:user:{user_id}"

    @property
    def users_set_key(self) -> str:
        """
        Returns a Redis key for the set of all users.

        The key is constructed by concatenating the prefix and "users".
        """
        return f"{self.prefix}:users"

    async def is_authorized(self, user_id: int) -> bool:
        """
        Checks if a user with the given ID is authorized (i.e., exists in Redis.

        Args:
            user_id (int): User ID to check.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        return await self.redis.exists(self._user_key(user_id)) > 0

    async def is_admin(self, user_id: int) -> bool:
        """
        Checks if a user with the given ID has the 'admin' role.

        Args:
            user_id (int): User ID to check.

        Returns:
            bool: True if the user has the 'admin' role, False otherwise.
        """
        role = await self.redis.hget(self._user_key(user_id), "role")  # type: ignore
        return role is not None and role.decode() == "admin"

    async def add_user(
        self,
        user_id: int,
        full_name: str = "",
        role: str = "user",
        added_by: Optional[int] = None,
        notes: str = "",
    ) -> bool:
        """
        Adds a user to the authorization system.

        Args:
            user_id (int): The user ID to add.
            full_name (str): The user's full name. Defaults to "".
            role (str): The user's role. Defaults to "user".
            added_by (Optional[int]): The user ID of the user who added this user. Defaults to None.
            notes (str): Any additional notes about the user. Defaults to "".

        Returns:
            bool: True if the user was added successfully, False otherwise.
        """
        key = self._user_key(user_id)

        # Don't overwrite existing user
        if await self.redis.exists(key):
            return False

        data = {
            "id": str(user_id),
            "full_name": full_name,
            "role": role,
            "added_by": str(added_by) if added_by is not None else "",
            "added_at": datetime.now(timezone.utc).isoformat(),
            "notes": notes,
        }

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.hset(key, mapping=data)
            pipe.sadd(self.users_set_key, user_id)
            await pipe.execute()

        return True

    async def remove_user(self, user_id: int) -> bool:
        """
        Removes a user from the authorization system.

        Args:
            user_id (int): The user ID to remove.

        Returns:
            bool: True if the user was removed successfully, False otherwise.
        """
        key = self._user_key(user_id)
        if not await self.redis.exists(key):
            return False

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.delete(key)
            pipe.srem(self.users_set_key, user_id)
            await pipe.execute()

        return True

    async def get_list_users(self) -> dict[int, dict]:
        """
        Retrieves a list of all registered users.

        Returns a dictionary where keys are user IDs and values are dictionaries
        containing user details.

        Note: This function currently retrieves all users one by one, which may be
        inefficient if there are many users. Improving the performance of this function
        is a TODO task.

        Returns:
            dict[int, dict]: A dictionary containing all registered users.
        """
        ids = await self.redis.smembers(self.users_set_key)  # type: ignore
        result: dict[int, dict] = {}

        if not ids:
            return result

        # ids is a set of bytes, convert to int
        user_ids = [int(i) for i in ids]

        # can do one by one, if users are not many
        # TODO: improve users retrieval performance if users can be many
        for uid in user_ids:
            key = self._user_key(uid)
            raw = await self.redis.hgetall(key)  # type: ignore
            if not raw:
                continue
            # decode to normal dict[str, str] and save
            result[uid] = {
                **{k.decode(): v.decode() for k, v in raw.items()},  # type: ignore
                "id": uid,
            }

        return result

    async def get_role(self, user_id: int) -> str:
        """
        Retrieves the role of a user with the given ID.

        Args:
            user_id (int): The ID of the user to retrieve the role for.

        Returns:
            str: The role of the user, or "viewer" if the user is not found.
        """
        role = await self.redis.hget(self._user_key(user_id), "role")  # type: ignore
        return role.decode() if role is not None else "viewer"
