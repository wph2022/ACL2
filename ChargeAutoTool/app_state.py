from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppState:
    mode: str = "log_search"
    selected_file: str | None = None
    selected_folder: str | None = None
    selected_tab: str = "result"
    parse_result: dict[str, Any] = field(default_factory=dict)
    status_message: str = "Ready"
