"""Top level module tests."""
from doggo_discriminator import __version__


def test_version() -> None:
    """Test tha the module version is the expected version."""
    assert __version__ == "0.1.0"
