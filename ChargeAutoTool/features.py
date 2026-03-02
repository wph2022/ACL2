from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class FeatureFacade:
    rules: dict

    def search_log(self, text: str, keyword: str) -> list[str]:
        return [line for line in text.splitlines() if keyword in line]

    def parse_healthd(self, text: str) -> dict:
        pattern = re.compile(r"healthd:\s*(.*)")
        rows = [m.group(1) for m in map(pattern.search, text.splitlines()) if m]
        return {"count": len(rows), "items": rows[:50]}

    def parse_vbat(self, text: str) -> dict:
        pattern = re.compile(r"vbat[:=]\s*(\d+)", re.IGNORECASE)
        vals = [int(v) for v in pattern.findall(text)]
        return {"samples": len(vals), "min": min(vals) if vals else None, "max": max(vals) if vals else None}

    def generate_curve_points(self, text: str) -> list[tuple[int, int]]:
        pattern = re.compile(r"(\d+)\s*,\s*(\d+)")
        return [(int(a), int(b)) for a, b in pattern.findall(text)]

    def analyze_ai_protocol(self, text: str) -> dict:
        tags = self.rules.get("ai_protocol_tags", ["REQ", "RSP", "ERR"])
        counts = {tag: text.count(tag) for tag in tags}
        return {"tags": counts}

    def analyze_register_dump(self, text: str) -> dict:
        reg_map = self.rules.get("register_map", {})
        decoded = {}
        for addr, name in reg_map.items():
            m = re.search(rf"{addr}\s*[:=]\s*(0x[0-9A-Fa-f]+|\d+)", text)
            if m:
                decoded[name] = m.group(1)
        return decoded
