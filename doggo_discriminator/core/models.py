"""Core Data Structures used in by the application."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class Identifiable(BaseModel):
    """Mixin Class that adds a unique identifier field to a dataclass.

    This uuid will be generated on assingment.

    Attributes:
        id: (uuid.UUID) a uuid4 compliant unique identifer
    """

    id: UUID = Field(default_factory=uuid4)

    def __eq__(self, __o: object) -> bool:
        """Boolean test for equality.

        This overrides the == operator to that to Identifiables
            are of the same class and have matching ids.

        Args:
            __o (object): the right hand operand for ==

        Raises:
            NotImplementedError: if the method is called with right hand operand
                that is not an Identifiable.

        Returns:
            bool: whether the objects have the same identifier and are of like type.
        """
        if not isinstance(__o, Identifiable):
            raise NotImplementedError(
                "Identifiables only support comparison to other identifiables"
            )
        elif type(self) is not type(__o):
            return False
        else:
            return self.id == __o.id


class BaseLabeler(Identifiable):
    """Base class for a labeler.

    Attributes:
        name: a name for the labeler.
        email: an email address for the labeler.
    """

    name: Optional[str]
    email: Optional[EmailStr]


class BaseLabel(Identifiable):
    """Base Class representing a lablel for value.

    Attributes:
        name: (str) a name for the label
        value: (typing.Any) the value of the label subclasses should override
            this is a more specific type
    """

    name: str
    value: Any


class BaseDatum(Identifiable):
    """A base class for a data item to be labeled.

    Attributes:
        value (typing.Any) the value of the of the datum
    """

    value: Any


class LabelAssingment(Identifiable):
    """Class representing the assignemetn of a label to a dataum."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    datum: BaseDatum
    labeler: BaseLabeler
    label: BaseLabel


class LabeledDatum(BaseDatum):
    """Class Representing a data item with one or more labels.

    Labels may be assigned to it via the record_label method. Labels may optionally set
        a label as the ground_truth via the ground_label prooperty.

    Attributes:
        ground_label: (Optional[BaseLable]) a known accepted label for the data item
        assignments (List[LabelAssignment]) a list of Label Assignments associated
            to the data item. Use this to record potentially noisy labels from multiple
            labelers.
    """

    ground_label: Optional[BaseLabel]
    assignments: List[LabelAssingment]

    def base(self) -> BaseDatum:
        """Returns an unlabeled version of this datum."""
        return BaseDatum(id=self.id, value=self.value)

    @staticmethod
    def from_base_datum(
        base: BaseDatum,
        ground_label: Optional[BaseLabel] = None,
        assignments: Optional[List[LabelAssingment]] = None,
    ) -> LabeledDatum:
        """Static method for constucting a new LabeledDatum for a BaseDatum.

        The new Labeled datum will have the same id and value as the base

        Args:
            base (BaseDatum): the base datum to used

        Returns:
            LabeledDatum: a new LabeledDatum with no assigned labels.
        """
        return LabeledDatum(id=base.id, value=base.value, assignments=[])

    def record_label(self, labeler: BaseLabeler, label: BaseLabel) -> LabelAssingment:
        """Create a new LabelAssignment and add it to the list of label assingments.

        The datum field of the assignment will be stored as a BaseDatum with identical
        id and value to the calling object.

        Args:
            labeler (BaseLabeler): the labeler performing the assingment.
            label (BaseLabel): the label beign assinged.

        Returns:
            LabelAssingment: for conveniance this method return the new lable assinment.
        """
        new_assignment: LabelAssingment = LabelAssingment(
            labeler=labeler, label=label, datum=self.base()
        )

        self.assignments.append(new_assignment)
        return new_assignment
