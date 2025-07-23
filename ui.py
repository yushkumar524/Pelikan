import chess.svg
import os
import webbrowser

class UI:
    def __init__(self, board):
        self.board = board
        self.page_opened = False
        self.board_updated = False

    def display(self):
        svg = chess.svg.board(board=self.board, size=400)
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pelikan</title>
            <meta http-equiv="refresh" content="3">
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                }}
            </style>
            <script>
                function checkForUpdates() {{
                    fetch('board_signal.txt?t=' + Date.now())
                        .then(response => response.text())
                        .then(data => {{
                            if (data.trim() === 'true') {{
                                location.reload();
                            }}
                        }})
                        .catch(error => {{}})
                }}
                setInterval(checkForUpdates, 200);
            </script>
        </head>
        <body>
            {svg}
        </body>
        </html>
        '''
        filepath = os.path.abspath("chess_board.html")
        with open(filepath, "w") as f:
            f.write(html_content)
        
        signal_path = os.path.abspath("board_signal.txt")
        with open(signal_path, "w") as f:
            f.write(str(self.board_updated).lower())
        
        if not self.page_opened:
            webbrowser.open("file://" + filepath, new=0)
            self.page_opened = True
        
        self.board_updated = False

    def signal_board_update(self):
        self.board_updated = True

    def get_player_move(self):
        return input("Your move: ")