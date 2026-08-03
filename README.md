# T-Rex on the Rio–Antirrio Bridge

A playable Pygame platform adventure inspired by the Rio–Antirrio Bridge and Patras in Greece.

## Run

1. Use Python 3.13 (Pygame does not yet provide a macOS wheel for Python 3.14).
2. Create and activate an environment with `python3.13 -m venv .venv` then `source .venv/bin/activate`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Launch with `python main.py`.

## Controls

- `Space` or `Up Arrow`: jump
- `Down Arrow`: crouch under classroom desks
- `Left Ctrl`: throw a weapon during velociraptor encounters
- `Left Shift`: interact with the apatosaurus or Patras bench
- `Space` or click: restart after game over

## Project layout

- `main.py`: small application entry point.
- `game.py`: game state, progression, menus, HUD, and input loop.
- `backgrounds.py`: procedural scenes for each world.
- `entities.py`: player, enemies, collectibles, and platforms.
- `config.py`: shared constants and asset paths.
- `sprites/`: all PNG sprite assets.

## Next steps

Add new worlds by creating a background in `backgrounds.py`, game objects in `entities.py`, and a transition in `game.py`.




commands to run 

rm -rf ~/.buildozer/android/platform/ 
rm -rf .buildozer/ ~/.buildozer/ 


docker run --rm -it --platform linux/amd64 \
  -v "$(pwd)":/home/user/hostcwd \
  -v ~/.buildozer:/home/user/.buildozer \
  --entrypoint /bin/bash \
  kivy/buildozer:latest -c "
    echo 'import ssl; ssl._create_default_https_context = ssl._create_unverified_context' > \$(python3 -c 'import site; print(site.getsitepackages()[0])')/sitecustomize.py
    buildozer android debug
  "