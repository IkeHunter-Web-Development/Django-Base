"""
Faker Library
Used to generate fake data for unit testing.

Docs:
- https://faker.readthedocs.io/en/master/
- https://dev.to/ankitmalikg/python-generate-fake-data-with-faker-1ecj
"""

from faker import Faker


fake = Faker("en_US")


def fake_words(count: int = 2):
    """Create a string with fake words."""
    return " ".join(fake.words(3, unique=True))


__all__ = ["fake"]
