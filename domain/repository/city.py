from typing import List
from abc import ABC, abstractmethod

from domain.model import City


class ICityRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[City]:
        pass

    def find_by_id(self, id: str) -> City:
        pass

    @abstractmethod
    def find_by_geoid(self, geoid: str) -> City:
        pass

    @abstractmethod
    def find_by_name(self, name: str, state: str) -> City:
        pass

    @abstractmethod
    def add(self, city: City) -> City:
        pass
