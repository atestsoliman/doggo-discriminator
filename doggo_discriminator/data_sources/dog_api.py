"""A data source that fetches dogs for labeling.

Images are fetched from the dog.ceo dog api
The images are drawn from the Standford Dogs dataset
See: https://dog.ceo/dog-api/
"""
from typing import Optional

from pydantic import BaseModel, HttpUrl, parse_obj_as
from requests import Session

from doggo_discriminator.core.models import BaseDatum


class Dog(BaseModel):
    """Simple class for dog images.

    message (HttpURL) image URL as returned byu the dog api
    """

    message: HttpUrl


class DogSource:
    """Class for a basic source of dog images.

    This is meant as an example of a source interface. It has several short coming
    such as the (small) probabiliy of fetching duplicate images over a long batch
    of labeling.
    """

    session: Session
    url: str

    def __init__(self, session: Optional[Session] = None) -> None:
        """Constucts a new DogSource.

        Args:
            session (Optional[Session]): a custom session object to use.
                Use when needing to set proxies or specify custom a ca file, such as is
                commonly needed behind corportate firwalls. Defaults to None.
        """
        self.url = "https://dog.ceo/api/breeds/image/random"
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def fetch(self) -> BaseDatum:
        """Return a new BaseDatum containing a dog.

        Returns:
            BaseDatum: a new dog ready to be labled.
        """
        return BaseDatum(value=parse_obj_as(Dog, self.session.get(self.url).json()))
