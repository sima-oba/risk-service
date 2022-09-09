from dataclasses import dataclass, asdict
from datetime import datetime
from uuid import uuid4


@dataclass
class Model:
    _id: str
    created_at: datetime
    updated_at: datetime

    def asdict(self) -> dict:
        return asdict(self)

    @classmethod
    def new(cls, data: dict):
        return cls(
            _id=str(uuid4()),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **data
        )
