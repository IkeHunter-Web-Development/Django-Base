"""
Global formatting utility functions.
"""


def plural_noun(count_target: list | int, singular: str, plural: str = None):
    """
    Takes a list or number and will return singlar form if 1, plural form otherwise.

    Parameters
    ----------
        - count_target (list | int): List of items or count of items.
        - singular (str): Singular form of the noun.
        - plural (str): Plural form of the noun.
            If not provided, will add 's' to singular form.

    Examples
    --------
    >>> plural_noun(1, "apple")
    "apple"
    >>> plural_noun(2, "apple")
    "apples"
    >>> plural_noun(["apple"], "category", "categories")
    "category"
    >>> plural_noun(["apple", "banana"], "category", "categories")
    "categories"
    """

    plural = plural if plural else f"{singular}s"
    count = count_target

    if isinstance(count_target, list):
        count = len(count_target)

    return plural if count != 1 else singular
