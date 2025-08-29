from aiogram.types import Message
from logging import Logger
from re import compile, IGNORECASE
from typing import Optional

from lexicon.lexicon import get_message

INV_PATTERN = compile(r"^\d{5}(?:M)?$", IGNORECASE)  # Example: 12345 or 12345M


def is_valid_inv_name(inv: str) -> bool:
    """
    Validates the format of an inventory number.

    This function checks if the provided inventory number matches the expected format using a regular expression.
    Provided inventory numbers should be either 5 digits or 5 digits followed by an 'M' (case insensitive).

    Args:
        inv (str): The inventory number to validate.

    Returns:
        bool: True if the inventory number is valid, False otherwise.
    """

    return bool(INV_PATTERN.fullmatch(inv))


async def validate_inv_format(
    inv_lines: list[str], message: Message, logger: Logger
) -> Optional[bool]:
    """
    Validates a list of inventory numbers and sends an error message if any are invalid.

    This function checks each inventory number in the provided list for validity. If any invalid numbers are found,
    it logs a warning and sends an error message to the user

    Args:
        inv_lines (list[str]): List of inventory numbers to validate.
        message (Message): The incoming message that triggered the validation.
        logger (Logger): The logger instance for logging events.

    Returns:
            Optional[bool]: True if all inventory numbers are valid, False if any are invalid, None if the list is empty.
    """

    invalid_invs = [inv for inv in inv_lines if not is_valid_inv_name(inv)]
    if invalid_invs:
        logger.warning(
            f"User {message.from_user.full_name} ({message.from_user.id}) "  # type: ignore
            f"provided invalid inventory numbers: {', '.join(invalid_invs)}"
        )
        await message.answer(
            get_message("error_inv_format")[0]
            + "\n".join(f"• {inv}" for inv in invalid_invs)
            + get_message("error_inv_format")[1],
            parse_mode="HTML",
        )
        return False

    return True
