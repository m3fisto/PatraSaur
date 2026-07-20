# T-Rex on the Rio–Antirrio Bridge

A playable Pygame endless runner inspired by the Rio–Antirrio Bridge in Greece. It uses procedural placeholder graphics, so no external assets are required.

## Run

1. Use Python 3.13 (Pygame does not yet provide a macOS wheel for Python 3.14).
2. Create and activate an environment with `python3.13 -m venv .venv` then `source .venv/bin/activate`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Launch with `python main.py`.

## Controls

- `Space` or `Up Arrow`: jump
- `Down Arrow`: duck under seagulls
- `R`: restart after a collision

## Next steps

Replace the procedural drawing in `main.py` with files from an `assets/` directory when the final T-Rex, bridge, and obstacle art is ready.