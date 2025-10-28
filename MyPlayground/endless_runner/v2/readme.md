## Endless Runner — Pygame + SQLite
A teaching project demonstrating:
- Pygame game loop & state machine
- Endless runner mechanics with increasing difficulty
- SQLite high score persistence
- Clean multi‑file architecture


### Run the Game
```bash
pip install pygame
python main.py
```


### Windows Packaging
```bash
python -m pip install pyinstaller
python -m PyInstaller --noconsole --onefile --name EndlessRunner main.py
```
Generated executable will be in the `dist/` folder.


### Game Controls
- **Space / ↑** — Jump
- **R** — Restart (Game Over screen)
- **Enter** — Save name + return to menu (Game Over screen)
- **Esc** — Quit (Menu) / Return to Menu (during gameplay)


### Reset High Scores
To wipe all saved scores, delete the database file or execute:
```sql
DELETE FROM scores;
```
Database path per OS:
- **Windows**: `%LOCALAPPDATA%/EndlessRunner/scores.db`
- **macOS**: `~/Library/Application Support/EndlessRunner/scores.db`
- **Linux**: `~/.endlessrunner/scores.db`


> Pro tip: Instead of deleting rows you can wipe the table entirely:
```sql
DROP TABLE IF EXISTS scores;
```
(Will auto‑recreate on next launch)