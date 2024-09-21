#Color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def print_debug(message, is_error=False, is_warning=False):
    color = RED if is_error else (YELLOW if is_warning else GREEN)
    print(f"{color}[DEBUG] {message}{RESET}")