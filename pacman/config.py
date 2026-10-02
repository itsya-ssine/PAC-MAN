"""Configuration loading, comment stripping and validation."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("pacman.config")

MIN_LEVELS = 10
MAX_LEVELS = 100
MIN_WIDTH, MAX_WIDTH = 14, 40
MIN_HEIGHT, MAX_HEIGHT = 10, 40
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")


class ConfigError(Exception):
    """Raised when the configuration file cannot be used at all."""


@dataclass
class LevelConfig:
    """Size of one level's maze (in cells)."""

    width: int = 15
    height: int = 15


def default_levels() -> list[LevelConfig]:
    """Return the default list of ten growing levels."""
    return [LevelConfig(15 + i, 15 + i) for i in range(MIN_LEVELS)]


@dataclass
class Config:
    """Validated game settings (every field always holds a usable value)."""

    highscore_filename: str = "highscores.json"
    maze_module: str = "mazegen"
    maze_class: str = "MazeGenerator"
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    power_duration: float = 8.0
    ghost_respawn_time: float = 5.0
    player_speed: float = 7.0
    ghost_speed: float = 5.5
    cheat_mode: bool = False
    levels: list[LevelConfig] = field(default_factory=default_levels)

    @classmethod
    def load(cls, path: str) -> Config:
        """Read, clean and validate a config file.

        Args:
            path: path to a ``.json`` file (``#``, ``//`` and ``/* */``
                comments are allowed).

        Returns:
            A fully valid Config. Bad values are replaced by defaults
            (or clamped) and a message is logged for each one.

        Raises:
            ConfigError: if the file is missing, unreadable or is not
                a JSON object.
        """
        file = Path(path)
        if file.suffix.lower() != ".json":
            raise ConfigError(f"'{path}' is not a .json file")
        try:
            with file.open("r", encoding="utf-8") as handle:
                raw = handle.read()
        except FileNotFoundError:
            raise ConfigError(f"config file '{path}' not found") from None
        except (OSError, UnicodeDecodeError) as exc:
            raise ConfigError(f"cannot read '{path}': {exc}") from exc
        return cls.from_text(raw)

    @classmethod
    def from_text(cls, raw: str) -> Config:
        """Build a Config from the raw text of a config file."""
        try:
            data = json.loads(strip_comments(raw))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"invalid JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise ConfigError("the config must be a JSON object")
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        """Validate a decoded JSON object (unknown keys are ignored)."""
        d = Config()
        return cls(
            highscore_filename=_get_str(
                data, "highscore_filename", d.highscore_filename, False),
            maze_module=_get_str(data, "maze_module", d.maze_module, True),
            maze_class=_get_str(data, "maze_class", d.maze_class, True),
            lives=_get_int(data, "lives", d.lives, 1, 99),
            pacgum=_get_int(data, "pacgum", d.pacgum, 1, 5000),
            points_per_pacgum=_get_int(
                data, "points_per_pacgum", d.points_per_pacgum, 0, 100000),
            points_per_super_pacgum=_get_int(
                data, "points_per_super_pacgum",
                d.points_per_super_pacgum, 0, 100000),
            points_per_ghost=_get_int(
                data, "points_per_ghost", d.points_per_ghost, 0, 100000),
            seed=_get_int(data, "seed", d.seed, 0, 2**31 - 1),
            level_max_time=_get_int(
                data, "level_max_time", d.level_max_time, 5, 3600),
            power_duration=_get_float(
                data, "power_duration", d.power_duration, 1.0, 60.0),
            ghost_respawn_time=_get_float(
                data, "ghost_respawn_time", d.ghost_respawn_time, 1.0, 60.0),
            player_speed=_get_float(
                data, "player_speed", d.player_speed, 1.0, 20.0),
            ghost_speed=_get_float(
                data, "ghost_speed", d.ghost_speed, 1.0, 20.0),
            cheat_mode=_get_bool(data, "cheat_mode", d.cheat_mode),
            levels=_get_levels(data),
        )


def strip_comments(text: str) -> str:
    """Remove comments from JSON text.

    Lines whose first non-blank character is ``#`` are comments. ``//``
    and ``/* ... */`` comments are also accepted. Anything inside a
    JSON string is left untouched.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_string = False
    line_start = True
    while i < n:
        ch = text[i]
        if in_string:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == "#" and line_start:
            while i < n and text[i] != "\n":
                i += 1
            continue
        if text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            block = text[i:] if end == -1 else text[i:end + 2]
            out.append("\n" * block.count("\n") or " ")
            i += len(block)
            continue
        if ch == '"':
            in_string = True
        if ch == "\n":
            line_start = True
        elif not ch.isspace():
            line_start = False
        out.append(ch)
        i += 1
    return "".join(out)


def _get_int(data: dict[str, Any], key: str, default: int,
             low: int, high: int) -> int:
    """Return an int setting, clamped to [low, high] or the default."""
    if key not in data:
        log.warning("'%s' is missing, using default %s", key, default)
        return default
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, int):
        log.warning("'%s' must be an integer (got %r), using default %s",
                    key, value, default)
        return default
    if value < low or value > high:
        clamped = max(low, min(high, value))
        log.warning("'%s'=%s is out of range [%s, %s], using %s",
                    key, value, low, high, clamped)
        return clamped
    return value


def _get_float(data: dict[str, Any], key: str, default: float,
               low: float, high: float) -> float:
    """Return a numeric setting, clamped to [low, high] or the default."""
    if key not in data:
        log.warning("'%s' is missing, using default %s", key, default)
        return default
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        log.warning("'%s' must be a number (got %r), using default %s",
                    key, value, default)
        return default
    number = float(value)
    if not low <= number <= high:
        clamped = max(low, min(high, number))
        log.warning("'%s'=%s is out of range [%s, %s], using %s",
                    key, value, low, high, clamped)
        return clamped
    return number


def _get_bool(data: dict[str, Any], key: str, default: bool) -> bool:
    """Return a boolean setting or the default."""
    if key not in data:
        return default
    value = data[key]
    if not isinstance(value, bool):
        log.warning("'%s' must be true or false (got %r), using default %s",
                    key, value, default)
        return default
    return value


def _get_str(data: dict[str, Any], key: str, default: str,
             identifier: bool) -> str:
    """Return a string setting (optionally a Python identifier)."""
    if key not in data:
        log.warning("'%s' is missing, using default '%s'", key, default)
        return default
    value = data[key]
    if not isinstance(value, str) or not value.strip() or "\0" in value:
        log.warning("'%s' must be a non-empty string (got %r), "
                    "using default '%s'", key, value, default)
        return default
    value = value.strip()
    if identifier and not _IDENT.match(value):
        log.warning("'%s'=%r is not a valid Python name, using '%s'",
                    key, value, default)
        return default
    return value


def _get_levels(data: dict[str, Any]) -> list[LevelConfig]:
    """Return the validated level list (at least MIN_LEVELS entries)."""
    raw = data.get("levels")
    if raw is None:
        log.warning("'levels' is missing, using %d default levels",
                    MIN_LEVELS)
        return default_levels()
    if not isinstance(raw, list):
        log.warning("'levels' must be a list, using default levels")
        return default_levels()
    levels: list[LevelConfig] = []
    for index, item in enumerate(raw[:MAX_LEVELS], start=1):
        sub = item if isinstance(item, dict) else {}
        if not isinstance(item, dict):
            log.warning("level %d must be an object, using defaults", index)
        levels.append(LevelConfig(
            width=_get_int(sub, "width", 15, MIN_WIDTH, MAX_WIDTH),
            height=_get_int(sub, "height", 15, MIN_HEIGHT, MAX_HEIGHT),
        ))
    if len(levels) < MIN_LEVELS:
        log.warning("only %d level(s) configured, the game needs at least "
                    "%d: adding default levels", len(levels), MIN_LEVELS)
        for extra in default_levels()[len(levels):]:
            levels.append(extra)
    return levels
