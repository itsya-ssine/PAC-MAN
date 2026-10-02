"""Tests for configuration parsing and validation."""

from pathlib import Path

import pytest

from pacman.config import Config, ConfigError, strip_comments


def test_comments_are_removed() -> None:
    text = '# a comment\n{"lives": 5, // trailing\n/* block */"seed": 7}'
    cfg = Config.from_text(text)
    assert cfg.lives == 5
    assert cfg.seed == 7


def test_hash_inside_string_is_kept() -> None:
    cleaned = strip_comments('{"highscore_filename": "a#b//c.json"}')
    assert "a#b//c.json" in cleaned


def test_invalid_and_out_of_range_values() -> None:
    cfg = Config.from_dict({"lives": "many", "pacgum": -4,
                            "level_max_time": 10 ** 9, "extra": 1})
    assert cfg.lives == 3
    assert cfg.pacgum == 1
    assert cfg.level_max_time == 3600


def test_levels_are_padded_to_ten() -> None:
    cfg = Config.from_dict({"levels": [{"width": 20, "height": 12}]})
    assert len(cfg.levels) == 10
    assert (cfg.levels[0].width, cfg.levels[0].height) == (20, 12)


def test_level_sizes_are_clamped() -> None:
    cfg = Config.from_dict({"levels": [{"width": 3, "height": 999}]})
    assert (cfg.levels[0].width, cfg.levels[0].height) == (14, 40)


def test_bool_is_not_an_int() -> None:
    assert Config.from_dict({"lives": True}).lives == 3


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        Config.load(str(tmp_path / "nope.json"))


def test_wrong_extension(tmp_path: Path) -> None:
    file = tmp_path / "config.txt"
    file.write_text("{}")
    with pytest.raises(ConfigError):
        Config.load(str(file))


def test_broken_json_and_non_object() -> None:
    with pytest.raises(ConfigError):
        Config.from_text("{not json")
    with pytest.raises(ConfigError):
        Config.from_text("[1, 2]")


def test_shipped_config_is_valid() -> None:
    cfg = Config.load("config.json")
    assert cfg.lives == 3
    assert len(cfg.levels) >= 10
