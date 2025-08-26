from aiogram.types import Message
from logging import Logger
from re import compile, IGNORECASE
from typing import Optional

from lexicon.lexicon import get_message

INV_PATTERN = compile(r"^\d{5}(?:M)?$", IGNORECASE)  # Example: 12345 or 12345M


def is_valid_inv_name(inv: str) -> bool:
    """
    Validates the format of an inventory number.

    Args:
        inv (str): The inventory number to validate.
    Returns:
        bool: True if the inventory number is valid, False otherwise.
    """
    return bool(INV_PATTERN.fullmatch(inv))


async def validate_inv_format(
    inv_lines: list[str], message: Message, logger: Logger
) -> Optional[bool]:
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
