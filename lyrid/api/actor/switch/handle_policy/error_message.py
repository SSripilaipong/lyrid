def invalid_argument_for_function_error(argument_name: str, function_name: str):
    return TypeError(f"'{argument_name}' is an invalid argument for method '{function_name}'")
