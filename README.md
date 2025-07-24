# Pelikan 𓅟
A Python-based chess engine with a command-line interface, SVG board visualization, alpha-beta pruning, and opening book support.

## Features

- Opening book using Polyglot (.bin) format
- Alpha-beta pruning and transposition table with Zobrist hashing to increase efficiency
- Quiescence search to increase quality of play
- SVG-based UI that updates in browser

## Getting Started

### Requirements

- Python 3.8+
- `python-chess`: Install via pip:

  ```bash
  pip install chess
  ```

### Clone the Repo

  ```bash
  git clone https://github.com/yushkumar524/Pelikan.git
  cd Pelikan
  ```

### Run the Engine

  ```bash
  python main.py
  ```

### Choose your side and play!

You'll be prompted to play either white ('w') or black ('b'). The engine responds with its own move after each turn. The current game state will be displayed in the window with the SVG in your browser.
