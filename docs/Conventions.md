# Project Conventions

- App names are **plural**
- Model names are **singular**
- API viewsets go in `viewsets.py`
- Functional views go in `views.py`
- Services go in `services.py`

## Doc Strings

Example:

```py
"""
This represents a model for
how documentation should be structured.

Conventions adopted from:
    - Django
    - Kafka Python
"""


def example_function():
    """
    Function summary statement.

    Parameters
    ----------
        param_1 (int): First parameter details.
        param_2 (str): Second parameter details. This one
            has a long description, so needs indentation.
    """
    pass
```
