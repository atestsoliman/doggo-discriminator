"""Tests for the json_sink module."""
from pathlib import Path
from typing import Generator, List

from pydantic import parse_raw_as
from pytest import fixture

from doggo_discriminator.core.models import BaseLabel, BaseLabeler, LabeledDatum
from doggo_discriminator.data_sinks.json_sink import JSONLSink


@fixture
def local_file_sink_path() -> Generator[Path, None, None]:
    """Fixture that creates path for a sink file in the current working dir.

    The fixture deletes the path as part of the tear down
    """
    path = Path.cwd() / "testsink.jsonl"
    yield path
    path.unlink(missing_ok=True)


@fixture
def list_of_labeled_data() -> List[LabeledDatum]:
    """Fixture that returns a list of labele data."""
    labeler = BaseLabeler(name="test", email="test@example.org")
    label1 = BaseLabel(name="is_red", value=True)
    label2 = BaseLabel(name="is_red", value=False)

    labeled1 = LabeledDatum(value="cherry", assignments=[])
    labeled2 = LabeledDatum(value="banana", assignments=[])

    labeled1.record_label(labeler=labeler, label=label1)
    labeled2.record_label(labeler=labeler, label=label2)

    return [labeled1, labeled2]


def test_sink_labels(
    local_file_sink_path: Path, list_of_labeled_data: List[LabeledDatum]
) -> None:
    """Test that lines are writen and a can be read back."""
    sink = JSONLSink(local_file_sink_path)
    sink.write(list_of_labeled_data)

    with open(local_file_sink_path, "r") as f:
        lines = f.readlines()

        assert len(lines) == 2

        for line, item in zip(lines, list_of_labeled_data):
            assert item == parse_raw_as(LabeledDatum, line)


def test_sink_labels_overwrite(
    local_file_sink_path: Path, list_of_labeled_data: List[LabeledDatum]
) -> None:
    """Test that lines are writen and a can be read back."""
    sink = JSONLSink(local_file_sink_path)
    sink.write(list_of_labeled_data)
    sink.write(list_of_labeled_data, overwrite=True)

    with open(local_file_sink_path, "r") as f:
        lines = f.readlines()

        assert len(lines) == 2

        for line, item in zip(lines, list_of_labeled_data):
            assert item == parse_raw_as(LabeledDatum, line)


def test_sink_labels_append(
    local_file_sink_path: Path, list_of_labeled_data: List[LabeledDatum]
) -> None:
    """Test that lines are writen and a can be read back."""
    sink = JSONLSink(local_file_sink_path)
    sink.write(list_of_labeled_data)
    sink.write(list_of_labeled_data, overwrite=False)

    with open(local_file_sink_path, "r") as f:
        lines = f.readlines()

        assert len(lines) == 4
