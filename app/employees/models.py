from datetime import date

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Employee(Base):
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )

    department: Mapped["Department"] = relationship(back_populates="employees")  # type: ignore # noqa: F821

    __table_args__ = (
        UniqueConstraint("full_name", "department_id", name="uq_employee_name_department"),
    )
