from .base import BaseCollector
from .france_travail import FranceTravailCollector
from .rss_collector import RSSJobCollector
from .local_annecy import LocalAnnecyCollector
from .osv_collector import OSVCollector

__all__ = ["BaseCollector", "FranceTravailCollector", "RSSJobCollector", "LocalAnnecyCollector", "OSVCollector"]
