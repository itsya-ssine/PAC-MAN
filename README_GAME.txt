PAC-MAN  (42 project)

LAUNCH
  ./pacman config.json      (config.json is next to the program)

CONTROLS
  Arrows / WASD / ZQSD   move (menus: up / down)
  Space or Enter         start / confirm
  P or Esc               pause / resume
  C                      toggle cheat mode
    I invincible, N next level, F freeze ghosts, L extra life,
    B speed boost, G edible ghosts, T only 5 seconds left
  End of game: type your name (max 10 letters/digits/spaces), Enter

OPTIONS (config.json; '#' lines are comments)
  lives, pacgum, points_per_pacgum, points_per_super_pacgum,
  points_per_ghost, seed, level_max_time, power_duration,
  ghost_respawn_time, player_speed, ghost_speed, cheat_mode, levels
  Missing or invalid values fall back to safe defaults.

Highscores are saved in highscores.json (top 10).
