"""Test do the dog api source."""
from requests import Session

from doggo_discriminator.data_sources.dog_api import DogSource


def test_fetch_dog() -> None:
    """Tests the fetch method of DogSource."""
    src = DogSource()

    dog_data = src.fetch()

    assert dog_data.value.message


def test_passed_session() -> None:
    """Tests that the DogSource will accept a Session object."""
    src = DogSource(session=Session())

    dog_data = src.fetch()

    assert dog_data.value.message
