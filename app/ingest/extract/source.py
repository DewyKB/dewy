from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ExtractSource:
    url: str
    """The source URL to load from."""

    extra_info: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""

    extract_tables: bool = False
    """Whether to extract tables."""

    extract_images: bool = False
    """Whether to extract tables."""
