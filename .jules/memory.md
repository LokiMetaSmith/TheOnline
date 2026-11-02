## Archived: 2026-11-02

* `typeclasses/artifacts.py` defines special items: `OrbOfAwakening` (modifies `LLMCharacter` autonomy) and `MemeticShard` (interactive object with shifting personalities via `ShardCmdSet`).
* The `web/` directory follows the modern Evennia structure (containing `admin`, `api`, `webclient`, `website`, `static`, and `templates` directories) rather than legacy `*_overrides` folders.
* Dependency management uses `requirements.txt`, which must include `setuptools`, `openai`, and `pytest` alongside `evennia`.
* The `LLMCharacter` typeclass utilizes `evennia.TICKER_HANDLER` for autonomous behavior (configurable via `self.db.auto_act_interval`) and persists conversation context in `self.db.chat_history`.
* LLM-controlled character logic is implemented in `typeclasses/llm_character.py` and `world/llm.py`, using the `openai` library and `evennia.utils.utils.run_async` for asynchronous operations.
* The repository is an Evennia game directory (initialized via `evennia --init`) containing standard folders like `server`, `typeclasses`, `web`, and `world`.
* A script `server/ensure_superuser.py` creates a default superuser (admin/admin) if one is missing, utilized by the setup automation script.
* Core typeclasses (e.g., `Account`, `Channel`) require explicit imports from their respective modules (e.g., `evennia.accounts.accounts.DefaultAccount`) rather than the top-level `evennia` package to avoid initialization errors in this environment.
* The game world, "The Whispering Vale," includes Oakhaven (Village), Whispering Woods, and The Ruined Watchtower, populated by NPCs defined in `world/prototypes.py` (`BARNABY`, `KAELEN`, `ELARA`).
* `web/urls.py` uses `django.urls.re_path` instead of `django.conf.urls.url` to maintain compatibility with Django 5.
* The project uses standard Evennia inheritance (`DefaultObject`, `DefaultCharacter`, `DefaultRoom`, `DefaultExit`) in `typeclasses/` and `world/gendersub.py`; dependencies on `evennia.contrib.ingame_python` and `Event*` classes have been removed.
* Both `run_evennia.sh` (Bash) and `run_evennia.ps1` (PowerShell) automate server setup and management, supporting flags for `--reset` (database rebuild via `server/ensure_superuser.py`) and `--test` (running `pytest`).
* The `OPENAI_API_KEY` and `OPENAI_MODEL` settings are configured in `server/conf/settings.py`.
* Development workflows rely on a `.venv` virtual environment in the project root, managed by startup scripts `run_evennia.sh` (Linux/macOS) and `run_evennia.ps1` (Windows).
* The `LLMCharacter` supports an `UPDATE_PROMPT:` protocol in API responses to permanently modify its persona (`self.db.npc_prompt`) and can execute direct game commands when `llm_autonomy_level` is set to "high".
* Custom game logic exists in `commands/` (including `containercommands.py`, `emotes.py`, `movecommands.py`) and `world/` (`gendersub.py`, `llm.py`).
* A custom `manage.py` script is required in the root directory to perform database migrations directly, bypassing the `evennia` launcher's database checks.
