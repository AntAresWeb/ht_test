from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Department(Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    children: Mapped[list["Department"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys=[parent_id],
    )

    parent: Mapped["Department | None"] = relationship(
        back_populates="children",
        remote_side=[id],
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_department_name_parent"),
        CheckConstraint("id != parent_id", name="chk_department_not_self_parent"),
        Index("ix_department_hierarchy", "parent_id", "id"),
    )
