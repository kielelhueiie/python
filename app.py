from flask import Flask, request, jsonify
import json

app = Flask(__name__)

WIN_LEN = 5

def evaluate_line(line, player):
    """ Calcule le score d'une seule ligne (horizontale, verticale ou diagonale) """
    s = "".join(line)
    opp = 'X' if player == 'O' else 'O'
    score = 0
    
    if player*5 in s: return 1000000 
    if "." + player*4 + "." in s: score += 100000 
    if "." + player*3 + "." in s: score += 5000 
    
    if opp*5 in s: return -1000000
    if "." + opp*4 + "." in s: score -= 90000 
    if "." + opp*3 + "." in s: score -= 4000
    
    return score

def get_best_move(grid, size=20):
    best_score = -float('inf')
    move = (size // 2, size // 2)
    
    candidates = []
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '_':
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] != '_':
                            candidates.append((r, c))
                            break
                    if (r,c) in candidates: break
    
    if not candidates: return (size // 2, size // 2)

    for r, c in candidates:
        current_move_score = 0
        grid[r][c] = 'O'
        
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            line = []
            for i in range(-4, 5):
                nr, nc = r + i*dr, c + i*dc
                if 0 <= nr < size and 0 <= nc < size:
                    line.append(grid[nr][nc])
            current_move_score += evaluate_line(line, 'O')
            current_move_score += abs(evaluate_line(line, 'X'))
            
        grid[r][c] = '_'
        
        if current_move_score > best_score:
            best_score = current_move_score
            move = (r, c)
            
    return move

@app.route('/get_move', methods=['POST'])
def play():
    data = request.json
    grid = data.get('grid')
    size = len(grid)
    
    row, col = get_best_move(grid, size)
    return jsonify({"row": row, "col": col})

if __name__ == "__main__":
    app.run()
