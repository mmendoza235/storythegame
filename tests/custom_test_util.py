"""
Utility functions used to augment nosetest output.
"""


def output_divider(function_name, subtitle='START'):
    print_divider = "=" * 10
    leading_divide = "\n" + print_divider + " "
    trailing_divide = " " + print_divider + "\n"

    print leading_divide + function_name + ": " + subtitle + trailing_divide
