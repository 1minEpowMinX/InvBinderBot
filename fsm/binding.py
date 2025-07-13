from aiogram.fsm.state import State, StatesGroup


class BindingInventory(StatesGroup):
    """
    Defines the states for the MAC binding process.
    This class inherits from StatesGroup and defines the states used in the FSM for binding inventory numbers to MAC addresses.
    """

    waiting_for_inventory_numbers = (
        State()
    )  # State where the bot waits for inventory numbers from the user
    waiting_for_confirmation = (
        State()
    )  # State where the bot waits for user confirmation after receiving inventory numbers
