from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from app.extensions import db
# from app.models.common import Metadata


class Brand(db.Model):  # type: ignore
    __tablename__ = 'brand'
    __table_args__ = (
        UniqueConstraint(
            'code',
            name='_brand_unique_constraint',
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
