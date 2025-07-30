# Pelikan 𓅟
A Python-based chess engine with a Flask-based web interface, featuring SVG board visualization, alpha-beta pruning, and opening book support.

## Features

- Flask-based web interface
- Polyglot opening book
- Alpha-beta pruning and transposition table with Zobrist hashing to increase efficiency
- Quiescence search to increase quality of play
- SVG-based board that updates in real time

## Getting Started

### Requirements

- Python 3.8+
- `python-chess` and `flask`: Install via pip:

  ```bash
  pip install chess flask
  ```

### Clone the Repo

  ```bash
  git clone https://github.com/yushkumar524/Pelikan.git
  cd Pelikan
  ```

### Run the Web interface

- Start the Flask server:

  ```bash
  python app.py
  ```

- Open your browser and navigate to:

  ```
  http://127.0.0.1:5001
  ```

### Choose your side and play!

Use the buttons to choose your color (White or Black). Click "Start Game" and enter moves in algebraic notation (e.g., `d4`, `Nf6`, `0-0`). Pelikan will automatically respond after each move.
