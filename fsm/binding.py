from aiogram.fsm.state import State, StatesGroup


class BindingInventory(StatesGroup):
    """
    States for the inventory binding process.

    This class defines the different states the bot can be in during the inventory
    binding process, such as waiting for inventory numbers and waiting for user confirmation.

    Attributes:
        waiting_for_inventory_numbers (State): State where the bot waits for inventory numbers from the user
        waiting_for_confirmation (State): State where the bot waits for user confirmation after receiving inventory numbers
    """

    waiting_for_inventory_numbers = (
        State()
    )  # State where the bot waits for inventory numbers from the user
    waiting_for_confirmation = (
        State()
    )  # State where the bot waits for user confirmation after receiving inventory numbers
