from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    line: int
    column: int

@dataclass(frozen=True)
class CodeSmell:
    rule_name: str
    description: str
    file_path: str
    position: Position
    severity: str  # "INFO", "WARNING", "CRITICAL"
