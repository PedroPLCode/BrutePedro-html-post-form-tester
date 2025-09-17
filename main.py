import sys
from typing import Literal


def main(mode: Literal["attack", "check"]) -> None:
    """Run the selected script based on the provided mode.

    Depending on the mode, this function will either run the attack
    script or the server check script.

    Args:
        mode (Literal["attack", "check"]): The mode to run.
            - "attack": runs the brute force attack script.
            - "check": runs the server pre-check script.

    Prints:
        Error message if the mode is invalid.
    """
    if mode == "attack":
        import core.attack as attack
        attack.run_brute_force_attack()
    elif mode == "check":
        import core.check as check
        check.check_server_before_brute_force()
    else:
        print("Invalid mode. Use 'attack' or 'check'.")


def cli() -> None:
    """Command-line interface entry point.

    Reads command-line arguments and executes the corresponding mode.
    Exits the program with a usage message if arguments are missing or invalid.

    Raises:
        SystemExit: If the number of arguments is not exactly 2.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py [attack|check]")
        sys.exit(1)
    mode_arg = sys.argv[1].lower()
    main(mode_arg)


if __name__ == "__main__":
    cli()
