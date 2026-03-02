from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class FeatureFacade:
    rules: dict[str, Any]

    def run(self, mode: str, text: str) -> dict[str, Any]:
        handlers = {
            "log_search": self.search_log,
            "healthd": self.parse_healthd,
            "vbat": self.parse_vbat,
            "curve": self.generate_curve_points,
            "ai_protocol": self.analyze_ai_protocol,
            "register": self.analyze_register_dump,
        }
        handler = handlers.get(mode)
        if not handler:
            return {"error": f"unsupported mode: {mode}"}
        return handler(text)

    def search_log(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("log_search", {})
        keywords = cfg.get("keywords", ["error"])
        ignore_case = cfg.get("ignore_case", True)
        flags = re.IGNORECASE if ignore_case else 0

        matched: list[str] = []
        for line in text.splitlines():
            if any(re.search(re.escape(kw), line, flags=flags) for kw in keywords):
                matched.append(line)

        return {"keywords": keywords, "count": len(matched), "items": matched[: cfg.get("max_items", 100)]}

    def parse_healthd(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("healthd", {})
        patterns = cfg.get("patterns", [r"healthd:\s*(.*)"])
        items: list[str] = []
        for raw in patterns:
            pattern = re.compile(raw)
            for line in text.splitlines():
                match = pattern.search(line)
                if match:
                    items.append(match.group(1) if match.groups() else match.group(0))
        return {"patterns": patterns, "count": len(items), "items": items[: cfg.get("max_items", 100)]}

    def parse_vbat(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("vbat", {})
        pattern = re.compile(cfg.get("pattern", r"vbat[:=]\s*(\d+)"), re.IGNORECASE)
        group_index = int(cfg.get("group", 1))
        values = [int(m.group(group_index)) for m in pattern.finditer(text)]
        return {
            "pattern": pattern.pattern,
            "samples": len(values),
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "avg": (sum(values) / len(values)) if values else None,
        }

    def generate_curve_points(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("curve", {})
        pattern = re.compile(cfg.get("pattern", r"(\d+)\s*,\s*(\d+)"))
        x_group = int(cfg.get("x_group", 1))
        y_group = int(cfg.get("y_group", 2))
        points = [(int(m.group(x_group)), int(m.group(y_group))) for m in pattern.finditer(text)]
        return {"pattern": pattern.pattern, "points": points, "count": len(points)}

    def analyze_ai_protocol(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("ai_protocol", {})
        tokens = cfg.get("tokens", ["REQ", "RSP", "ERR"])
        ignore_case = cfg.get("ignore_case", False)
        counts: dict[str, int] = {}
        for token in tokens:
            if ignore_case:
                counts[token] = len(re.findall(re.escape(token), text, flags=re.IGNORECASE))
            else:
                counts[token] = text.count(token)
        return {"tokens": tokens, "counts": counts}

    def analyze_register_dump(self, text: str) -> dict[str, Any]:
        cfg = self.rules.get("register", {})
        items = cfg.get("items", [])
        decoded: dict[str, str] = {}
        for item in items:
            addr = item.get("address")
            name = item.get("name", addr)
            value_pattern = item.get("value_pattern", r"(0x[0-9A-Fa-f]+|\d+)")
            if not addr:
                continue
            pattern = re.compile(rf"{re.escape(addr)}\s*[:=]\s*{value_pattern}")
            match = pattern.search(text)
            if match:
                decoded[name] = match.group(1)
        return {"count": len(decoded), "decoded": decoded}
