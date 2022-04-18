"""Test module for the core library covering the models module."""

from time import sleep
from uuid import uuid4

from pydantic import ValidationError
from pytest import fixture, raises

from doggo_discriminator.core.models import (
    BaseDatum,
    BaseLabel,
    BaseLabeler,
    LabelAssingment,
    LabeledDatum,
)
from doggo_discriminator.data_sources.dog_api import Dog, DogSource


@fixture
def new_labeler() -> BaseLabeler:
    """Fixture for crateing a base labeler tobe used in tests.

    Returns:
        BaseLabeler: a single BaseLabler instance
    """
    return BaseLabeler(name="test", email="test@example.org")


@fixture
def new_datum() -> BaseDatum:
    """Fixture for creating a base datum to be used in tests.

    Returns:
        BaseDatum: A single BaseDatum instance
    """
    return BaseDatum(value="This is a test sentence about dogs")


def test_labeler_email_validation() -> None:
    """Test that arbitrary strings are not accepted as values in the email field."""
    with raises(ValidationError):
        BaseLabeler(name="test", email="some-string that is not valid email.com")


def test_uuid_uniqueness() -> None:
    """Test that two instances using the UUID mixin compare as different."""
    first_datum = BaseDatum(value=1)
    second_datum = BaseDatum(value=1)

    assert first_datum == first_datum
    assert second_datum == second_datum
    assert first_datum != second_datum


def test_comapare_to_non_identifiable(new_datum: BaseDatum) -> None:
    """Tests behavior when attempting to compare identifiable to non-idenifiable."""
    with raises(NotImplementedError):
        assert new_datum == "This is an object that is not a subclass of identifiable"


def test_compare_differnt_identifiable_types(
    new_datum: BaseDatum, new_labeler: BaseLabeler
) -> None:
    """Tests that == is not true for different subclasses of that share a uuid."""
    test_uuid = uuid4()
    new_datum.id = test_uuid
    new_labeler.id = test_uuid

    assert new_datum != new_labeler


def test_label_assingment(new_datum: BaseDatum, new_labeler: BaseLabeler) -> None:
    """Test label creation.

    Test that 2 instantiations of label assignment are different both by id
        and that the timestamps differ.
    """
    label = BaseLabel(name="size_class", value="big_pupper")
    first_assingment = LabelAssingment(
        datum=new_datum, labeler=new_labeler, label=label
    )
    # This was excecuting too fast to observe the difference in creation time.
    sleep(1)
    second_assignment = LabelAssingment(
        datum=new_datum, labeler=new_labeler, label=label
    )

    assert first_assingment != second_assignment
    assert first_assingment.timestamp != second_assignment.timestamp


def test_record_label(new_datum: BaseDatum, new_labeler: BaseLabeler) -> None:
    """Test recording a label.

    The label and labler attrinutes should be identical to those passed to
        record label.
    """
    labeled = LabeledDatum.from_base_datum(new_datum)
    label = BaseLabel(name="is_dog", value=True)
    labeled.record_label(new_labeler, label)

    assert labeled.assignments[0].label == label
    assert labeled.assignments[0].labeler == new_labeler
    assert type(labeled.assignments[0].datum) is BaseDatum
    assert type(labeled.assignments[0].datum) is not LabeledDatum


def test_record_object_valued_label(new_labeler: BaseLabeler) -> None:
    """Tests that a data item with an object value has it's type preserved."""
    src = DogSource()
    object_datum = src.fetch()
    labeled = LabeledDatum.from_base_datum(object_datum)
    assert isinstance(labeled.value, Dog)
