import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
import enum
from typing import Optional, Annotated

metadata_obj = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )]
# declarative style
class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class ResumesOrm(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# imperative style
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_name", String),
)
# resumes_table = Table(
#     "resumes",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("title", String(256)),
#     Column("compensation", Integer, nullable=True),
#     Column("workload", Enum(Workload)),
#     Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
#     Column("created_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())")),
#     Column("updated_at", TIMESTAMP,server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow),
# )