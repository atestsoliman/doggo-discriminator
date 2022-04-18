"""A demo of a labeling application using the a source, a sink, and the core classes.

Could use better abstractions once they are implemented in the interface submodule
"""

from enum import Enum
from pathlib import Path

import requests
import typer
from PIL import Image

from doggo_discriminator.core.models import BaseLabel, BaseLabeler, LabeledDatum
from doggo_discriminator.data_sinks.json_sink import JSONLSink
from doggo_discriminator.data_sources.dog_api import Dog, DogSource


class LabelChoices(str, Enum):
    """Enumeration of possible lables in the application."""

    big_pupper = "b"
    small_doggo = "s"


source = DogSource()

sink = JSONLSink(Path.cwd() / "label_cache.jsonl")

app = typer.Typer()


def echo_dog(dog: Dog) -> None:
    """Prints a dog to the terminal.

    This bit of cutesey code was taken from:
    https://www.educative.io/edpresso/how-to-generate-ascii-art-from-image-using-python
    Printing Images of dogs to the terminal is not the focus of this exercise
    """
    with open("temp_dog.png", "wb") as temp_file:
        data = requests.get(dog.message).content
        temp_file.write(data)

    ascii_chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]

    image = Image.open("temp_dog.png")
    image = image.convert("L")
    width, height = image.size
    new_width = 100
    new_height = new_width * height // width
    image = image.resize((new_width, new_height))

    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ascii_chars[pixel // 25]

    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i : i + img_width] + "\n"
    typer.echo(ascii_img)


@app.command()
def show_random_dog() -> None:
    """Prints a random dog to the console, because people like dogs!"""
    echo_dog(source.fetch().value)


@app.command()
def label_dogs(
    name: str = typer.Option(..., prompt=True),  # noqa: B008
    email: str = typer.Option(..., prompt=True),  # noqa: B008
) -> None:
    """Runs a loop asking the user to label images of dogs."""
    dog_session = []
    new_labeler = BaseLabeler(name=name, email=email)

    while True:
        next_dog = source.fetch()

        echo_dog(next_dog.value)

        short_label = typer.prompt(
            "Is this small doggo [s] or a big pupper [b]?", type=LabelChoices
        )
        if short_label == LabelChoices.big_pupper:
            new_label = BaseLabel(name="dog_type", value="big_pupper")
        elif short_label == LabelChoices.small_doggo:
            new_label = BaseLabel(name="dog_type", value="small_doggo")
        else:
            typer.echo("Moving on...")
            continue

        typer.echo(f"Recording this good boy or girl as a {new_label.value}!")
        new_item = LabeledDatum.from_base_datum(next_dog)
        new_item.record_label(labeler=new_labeler, label=new_label)
        dog_session.append(new_item)

        quit_and_save = typer.confirm("quit and save?")
        if quit_and_save:
            sink.write(dog_session)
            break


if __name__ == "__main__":
    app()
