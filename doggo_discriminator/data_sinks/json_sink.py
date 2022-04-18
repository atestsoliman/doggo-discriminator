"""A simple data sink that writes Labeled data a file in JSON format."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from doggo_discriminator.core.models import LabeledDatum


class Sink(ABC):
    """Interface for a Sink.

    A sink must implement a write method that will write labeled data to some target
    """

    @abstractmethod
    def write(self, items: List[LabeledDatum]) -> None:
        """Abstract method for writing to a target, e.g., a file or a database."""


class JSONLSink(Sink):
    """Basic DataSink That stores Labeled Data as JSONLines."""

    filepath: Path

    def __init__(self, filepath: Path) -> None:
        """Construct a new JSONLSink.

        Args:
            filepath: (pathlib.Path) the path at which to write the file.
        """
        self.filepath = filepath
        super().__init__()

    def write(self, items: List[LabeledDatum], overwrite: bool = False) -> None:
        """Writes as list of labeled data to a the filepath in jsonlines format.

        Args:
            items (List[LabeledDatum]): the labeled data to write
            overwrite (bool, optional): whether to overwrite the file at file path if
            it exists  Defaults to False.
        """
        if overwrite:
            mode = "w"
        else:
            mode = "a"
        with open(self.filepath, mode) as sink:
            for item in items:
                sink.write(item.json())
                sink.write("\n")
