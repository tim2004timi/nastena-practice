from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    control_sum = Column(Integer, nullable=False)

    students = relationship(
        "Student",
        back_populates="group",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name={self.name})>"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fio = Column(String(255), nullable=False)
    score_1 = Column(String(1), nullable=True)
    score_2 = Column(String(1), nullable=True)
    score_3 = Column(String(1), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)

    group = relationship("Group", back_populates="students")

    __table_args__ = (
        CheckConstraint(
            "(score_1 IN ('5','4','3','2','н')) OR score_1 IS NULL",
            name="ck_students_score_1_values",
        ),
        CheckConstraint(
            "(score_2 IN ('5','4','3','2','н')) OR score_2 IS NULL",
            name="ck_students_score_2_values",
        ),
        CheckConstraint(
            "(score_3 IN ('5','4','3','2','н')) OR score_3 IS NULL",
            name="ck_students_score_3_values",
        ),
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, fio={self.fio}, group_id={self.group_id})>"


