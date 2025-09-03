const board = document.getElementById("board");
const num_cols = 7;
const num_rows = 6;
const inrow = 4;
let move = 1; //1 - player's move, 2 - agent's
let locked = 0;
const player_colour = "#ffdd78";
const agent_colour = "#ff7878";
const obs = {}
obs.board = []



function getAgentMove() {
  return new Promise(async (resolve) => {
    const data = {
        board: obs.board,
        num_cols: num_cols,
        num_rows: num_rows,
        inrow: inrow
    };
    const response = await fetch('/agent-make-move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const move = await response.json();
    resolve(move.move);
  });
}

function get_current_colour(){
  if(move==1) return player_colour;
  return agent_colour;
}

//function that creates a board
function create_board(){
  for(let i=0;i<num_rows;i++){
    const row = document.createElement('tr'); //create a row
    const obs_row = []; 
    for(let j=0;j<num_cols;j++){
      const cell = document.createElement('td'); //create a cell
      const cellId = `cell_${i}_${j}`; //cell id is cell_i_j
      cell.setAttribute('id', cellId);
      if(i==0){
        cell.classList.add('top-row') //if cell is on top, mark it with a classname
      }
      row.appendChild(cell); //append the cell to the row
      obs_row.push(0);
    }
    board.appendChild(row); //add the row to the board
    obs.board.push(obs_row);
  }
}

function update_board(){
  for(let i=0;i<num_rows;i++){
    for(let j=0;j<num_cols;j++){
      let cell = get_cell(i, j);
      if(obs.board[i][j]==0) cell.style.backgroundColor = '';
      else if(obs.board[i][j]==1) cell.style.backgroundColor = player_colour;      
      else if(obs.board[i][j]==2) cell.style.backgroundColor = agent_colour;
    }
  }
}

function get_coord(cell){
  let id = cell.id;
  id = id.split("_");
  const row = parseInt(id[1]);
  const col = parseInt(id[2]);
  return [row, col];
}

function cell_empty(cell){
  const coord = get_coord(cell);
  const row = coord[0];
  const col = coord[1];
  return obs.board[row][col]==0;
}

function cell_empty_coord(row, col){
  if (row<0 || row>=num_rows || col<0 || col>=num_cols) return false;
  return obs.board[row][col]==0;
}

function get_cell(row, col){
  const cellId = `cell_${row}_${col}`;
  const cell = document.getElementById(cellId);
  return cell;
}

//add colour to cell
function addBgColour(event){
  cell = event.target;
  if(cell_empty(cell)) cell.style.backgroundColor = get_current_colour();
}
function addBgColourCell(cell){
  if(cell_empty(cell)) cell.style.backgroundColor = get_current_colour();
}
//remove colour from cell
function removeBgColour(event){
  cell = event.target;
  if(cell_empty(cell)) cell.style.backgroundColor = '';
}
function removeBgColourCell(cell){
  if(cell_empty(cell)) cell.style.backgroundColor = '';
}

function gameFinished(){
  const players = [1, 2];
  let isFull = true;
  for (let player of players) {
      for (let row = 0; row < num_rows; row++) {
          for (let col = 0; col < num_cols; col++) {
              if (col <= num_cols - inrow) {
                  let countH = 0;
                  let countV = 0;
                  for (let k = 0; k < inrow; k++) {
                      if (obs.board[row][col + k] === player) countH++;
                      if (obs.board[col + k] && obs.board[col + k][row] === player) countV++;
                  }
                  if (countH === inrow || countV === inrow) return player; 
              }
              if (row <= num_rows - inrow) {
                  let countD1 = 0;
                  let countD2 = 0;
                  for (let k = 0; k < inrow; k++) {
                      if (obs.board[row + k] && obs.board[row + k][col + k] === player) countD1++;
                      if (obs.board[row + k] && obs.board[row + k][col - k] === player) countD2++;
                  }
                  if (countD1 === inrow || countD2 === inrow) return player; 
              }
              if (obs.board[row][col] === 0) isFull = false; 
          }
      }
  }
  if(isFull) return 3;
  return 0; 
}



async function makeAgentMove(){
  /*
  let cols = [];
  for(let i=0;i<num_cols;i++){
    if(cell_empty_coord(0,i)){
      cols.push(i);
    }
  }
  let x = Math.floor(Math.random() * cols.length);*/
  col = await getAgentMove();
  makeMove(0, col);
  locked = 0;
}


function makeMove(row, col){
  if(!cell_empty_coord(row, col)) return;
  cell = get_cell(row, col);
  addBgColourCell(cell);
  function showFall() {
    return new Promise(resolve => {
        if (!cell_empty_coord(row + 1, col)) {
            resolve();
            return;
        }
        removeBgColourCell(cell);
        row += 1;
        cell = get_cell(row, col);
        addBgColourCell(cell);

        setTimeout(() => {
            showFall().then(resolve);
        }, 50);
    });
  } 

  showFall().then(() => {
      obs.board[row][col] = move;
      move = 3 - move;

      update_board();

      let gamef = gameFinished();
      if(gamef!=0){
        locked = 1;
        if(gamef==1) alert("You won");
        if(gamef==2) alert("You lost");
        if(gamef==3) alert("Draw. No more space on the board");
      }
      if(move == 2 && gamef==0) makeAgentMove();

  });
}

function cellClicked(event){
  if(locked) return;
  locked = 1;
  let cell = event.target;

  const coord = get_coord(cell);
  let row = coord[0];
  let col = coord[1];

  makeMove(row, col);
}

function restartGame(){
  //clear_board();
  create_board();
}


restartGame();

//
const divElements = document.querySelectorAll('.top-row');
divElements.forEach(function(div) {
    div.addEventListener('mouseenter', addBgColour);
    div.addEventListener('mouseleave', removeBgColour);
    div.addEventListener('click', cellClicked);
});
