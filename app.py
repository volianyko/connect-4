from flask import Flask, request, render_template, jsonify
import minimax_agent
import mcts_agent


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/agent-make-move', methods=['POST'])
def agentMakeMove():
    data = request.json
    board = data['board']
    num_cols = data['num_cols']
    num_rows = data['num_rows']
    inrow = data['inrow']

    move = minimax_agent.move(board, num_cols, num_rows, inrow)
    #move = mcts_agent.move(board, num_cols, num_rows, inrow)

    return jsonify({
        "move": move
    })
    

if __name__ == '__main__':
    app.run(debug=True)