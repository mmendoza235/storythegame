"""
Utility functions used to augment nosetest output and increase readability.
"""


def output_divider(title, subtitle='START'):
    """
    Divides the nosetest output.
    Meant to be called at the beginning and end of each test.
    """
    divider = "=" * 10
    leading_divide = "\n" + divider + " "
    trailing_divide = " " + divider + "\n"

    print leading_divide + title + ": " + subtitle + trailing_divide
