"""
Utility functions and CLI interface.
"""

from .config import (
    DIFFICULTY_LEVELS,
    COMPREHENSIVE_DISTRIBUTION,
    VISUAL_SETTINGS,
    PDF_SETTINGS,
)
from .educational_utils import (
    EducationalUtils,
    MathUtils,
    format_time_estimate,
    get_encouragement_message,
)

try:
    from .visual_generator import visual_generator

    VISUAL_AVAILABLE = True
except ImportError:
    visual_generator = None
    VISUAL_AVAILABLE = False

__all__ = [
    "DIFFICULTY_LEVELS",
    "COMPREHENSIVE_DISTRIBUTION",
    "VISUAL_SETTINGS",
    "PDF_SETTINGS",
    "EducationalUtils",
    "MathUtils",
    "format_time_estimate",
    "get_encouragement_message",
    "visual_generator",
    "VISUAL_AVAILABLE",
]
