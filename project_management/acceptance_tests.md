# Acceptance test plan

| # | Feature | How to test | Expected | Result | Bug / fix |
|---|---|---|---|---|---|
| 1 | Launch | `python3 pac-man.py config.json` | Main menu | TODO | |
| 2 | Bad usage | no argument, 2 arguments, missing file, non-json file, broken JSON | Clear message, no traceback | TODO | |
| 3 | Config comments | `#`, `//`, `/* */` in config | Ignored | TODO | |
| 4 | Invalid values | wrong types, out-of-range, unknown keys, missing keys | Defaults/clamp + log, no crash | TODO | |
| 5 | Maze generation | level 1 with seed 42 twice | Same maze; later levels differ | TODO | |
| 6 | Generator failure | break the module name | Error shown, back to menu | TODO | |
| 7 | Player movement | arrows, WASD/ZQSD, walls | Moves in corridors only | TODO | |
| 8 | Pacgum / super-pacgum | eat them | Score +X / +Y, ghosts edible | TODO | |
| 9 | Ghosts | chase, flee when edible, eaten ghost respawns | +Z points, returns after delay | TODO | |
| 10 | Lives | touch a ghost | Life lost, respawn in the middle | TODO | |
| 11 | Time limit | wait / cheat T | Life lost, level restarted | TODO | |
| 12 | Levels | cheat N x10 | Score and lives kept, victory after last | TODO | |
| 13 | Pause | P / Esc | Game frozen; resume or main menu | TODO | |
| 14 | HUD | during play | Score, lives, level, time | TODO | |
| 15 | Game over / victory | lose / win | Final score + name entry | TODO | |
| 16 | Highscores | enter names, restart | Top 10 persisted, shown in menu | TODO | |
| 17 | Highscore file errors | delete / corrupt / read-only file | No crash | TODO | |
| 18 | Name rules | 11+ chars, symbols | Max 10, alphanumeric + spaces | TODO | |
| 19 | Cheat mode | C then I, N, F, L, B, G, T | Each cheat works | TODO | |
| 20 | Lint | `make lint` | No error | TODO | |
| 21 | Package | `make package`, run from itch.io build | Fully functional | TODO | |
