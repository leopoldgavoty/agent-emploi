from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCollector(ABC):
    """Classe de base pour un collecteur d'offres d'emploi."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Récupère et normalise une liste d'offres d'emploi."""
        pass
