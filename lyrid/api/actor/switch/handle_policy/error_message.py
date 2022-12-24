def invalid_argument_for_method_error(argument_name: str, method_name: str) -> TypeError:
    return TypeError(f"'{argument_name}' is an invalid argument for method '{method_name}'")


def argument_in_method_must_be_annotated_as_type_error(
        argument_name: str, method_name: str, type_name: str,
) -> TypeError:
    return TypeError(f"'{argument_name}' argument in method '{method_name}' must be annotated with type '{type_name}'")


def argument_in_method_must_be_included_as_type_error(
        argument_name: str, method_name: str, type_name: str,
) -> TypeError:
    return TypeError(f"'{argument_name}' argument in method '{method_name}' must be included with type '{type_name}'")
