"""
Utility functions used to augment nosetest output and increase readability.
"""


def output_divider(function_name, subtitle='START'):
    """
    Divides the nosetest output.
    Meant to be called at the beginning and end of each test.
    """
    print_divider = "=" * 10
    leading_divide = "\n" + print_divider + " "
    trailing_divide = " " + print_divider + "\n"

    print leading_divide + function_name + ": " + subtitle + trailing_divide
