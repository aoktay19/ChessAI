//scripts.js
let maxTime = 180;
let timerPlayer1;
let timerPlayer2;
let currentPlayer = 1;
let player1Time = maxTime; // 3 minutes in seconds
let player2Time = maxTime; // 3 minutes in seconds
let isplayingWithAI = false;

const moveHistory = [];
async function handleSquareClick(file, rank) {
    const fileChar = String.fromCharCode(97 + file);
    const rankChar = rank + 1;
    const square = fileChar + rankChar;

    // Make an asynchronous request to the backend
    try {
        const response = await fetch("/get_possible_moves", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ square: square })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const clickedSquare = document.querySelector(`.chess-board tr:nth-child(${9 - rank}) td:nth-child(${file + 2})`);

        if (clickedSquare != null) {
            const isHighlighted = clickedSquare.classList.contains('highlight');
            if (isHighlighted) {
                handleMove(clickedSquare.move);
                switchPlayer();
                const highlightedSquares = document.querySelectorAll('.highlight');
                highlightedSquares.forEach(square => square.classList.remove('highlight'));
                setTimeout(function () {
                    if (isplayingWithAI) {
                    handleMove("AIMove");
                }
                }, 1000);

            }
        }

        if (data.piece) {
            console.log(`Piece at ${square}. Possible moves: ${data.moves.join(", ")}`);

            // Remove previous highlights
            const highlightedSquares = document.querySelectorAll('.highlight');
            highlightedSquares.forEach(square => square.classList.remove('highlight'));

            // Highlight squares with possible moves
            data.moves.forEach(move => {
                const [a, b, file, rank] = move.split('');
                const fileIndex = file.charCodeAt(0) - 'a'.charCodeAt(0);
                const rankIndex = 9 - parseInt(rank);
                const cell = document.querySelector(`.chess-board tr:nth-child(${rankIndex + 1}) td:nth-child(${fileIndex + 2})`);
                cell.classList.add('highlight');
                cell.move = move;

            });
        } else {
            console.log(`No piece at ${square}`);
        }
    } catch (error) {
        console.error("Error:", error.message);
    }
}

async function handleMove(move) {

    // Make an asynchronous request to the backend to make the move
    try {
        const response = await fetch("/make_move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ move: move })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.new_piece_map) {
            // Update the frontend chessboard based on the new piece map
            updateChessboard(data.new_piece_map);

            updateMoveHistory(data.move);

            if (data.is_checkmate) {
                // If it is checkmate, show a popup
                setTimeout(function () {
                    window.alert("Checkmate! Game Over!");
                }, 10);

                //window.alert("Checkmate! Game Over!");

            }
        } else {
            console.log(`Invalid move: ${data.message}`);
        }
    } catch (error) {
        console.error("Error:", error.message);
    }
}

// Function to update the chessboard based on the new piece map
function updateChessboard(pieceMap) {
    const cells = document.querySelectorAll('.chess-board td');
    // Define a mapping of piece types to symbols
    const pieceTypeToSymbolBlack = {
        1: '♟',
        2: '♞',
        3: '♝',
        4: '♜',
        5: '♛',
        6: '♚'
    };
    const pieceTypeToSymbolWhite = {
        1: '♙',
        2: '♘',
        3: '♗',
        4: '♖',
        5: '♕',
        6: '♔'
    };

    cells.forEach((cell, index) => {

        const newIndex = 8 * (7 - Math.floor(index / 8)) + (index % 8)
        const piece = pieceMap[newIndex];
        var pieceSymbol;
        // Set the content of the cell based on the piece map
        if (piece) {
            if (piece.color) {
                pieceSymbol = pieceTypeToSymbolWhite[piece.piece_type];
            } else {
                pieceSymbol = pieceTypeToSymbolBlack[piece.piece_type];
            }
            cell.textContent = pieceSymbol;
        } else {
            cell.textContent = '';
        }
    });
}
function startNewGame() {
    // Add logic here to reset the chessboard or make any necessary initialization
    while (moveHistory.length > 0) {
        moveHistory.pop();
    }
    updateMoveHistoryView();
    handleMove("newGame");
    console.log("New game started!");
    showMessage("");
    player1Time = maxTime;
    player2Time = maxTime;
    currentPlayer = 1;
}

function undoMove() {
    // Add logic here to reset the chessboard or make any necessary initialization
    moveHistory.pop();
    if (isplayingWithAI) {
        moveHistory.pop()
        handleMove("undoMove");
    }
    updateMoveHistoryView();
    handleMove("undoMove");
    console.log("Undo Move");
    showMessage("");
}

function showMessage(message) {
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.textContent = message;
}


function updateMoveHistory(move) {
    if (!move) {
        return; // Don't update if move is undefined
    }
    moveHistory.push({
        notation: move
    });
    updateMoveHistoryView();
}
function updateMoveHistoryView() {
    const moveHistoryBox = document.getElementById("moveHistoryBox");

    // Clear existing content
    moveHistoryBox.innerHTML = "";

    // Create a list element
    const moveList = document.createElement("ul");

    // Loop through the indices of the move history
    for (let i = 0; i < moveHistory.length / 2; i++) {
        if (2 * i + 1 == moveHistory.length) {
            const move1 = moveHistory[2 * i];

            const moveItem = document.createElement("div");
            moveItem.innerHTML = `<span>${i + 1}. ${move1.notation}</span>`;
            // Append the list item to the list
            moveList.appendChild(moveItem);
        } else {
            const move1 = moveHistory[2 * i];
            const move2 = moveHistory[2 * i + 1];
            const moveItem = document.createElement("div");
            moveItem.innerHTML = `<span>${i + 1}. ${move1.notation} ${move2.notation}</span>`;

            // Append the list item to the list
            moveList.appendChild(moveItem);
        }
    }

    // Append the list to the move history box
    moveHistoryBox.appendChild(moveList);
}

// Global variables for timers


function startTimers() {
    timerPlayer1 = setInterval(updateTimer, 1000, 'timerValuePlayer1');
    timerPlayer2 = setInterval(updateTimer, 1000, 'timerValuePlayer2');
}

function updateTimer(timerId) {
    const timerElement = document.getElementById(timerId);

    if (currentPlayer === 1 && timerId === 'timerValuePlayer1') {
        player1Time--;
    } else if (currentPlayer === 2 && timerId === 'timerValuePlayer2'){
        player2Time--;
    }
    
    const minutes = Math.floor(timerId === 'timerValuePlayer1' ? player1Time / 60 : player2Time / 60);
    const seconds = timerId === 'timerValuePlayer1' ? player1Time % 60 : player2Time % 60;

    const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    timerElement.textContent = formattedTime;

    if (player1Time === 0 || player2Time === 0) {
        clearInterval(timerPlayer1);
        clearInterval(timerPlayer2);
        alert(`Player ${currentPlayer} has run out of time. Game over!`);
    }
    
}

function switchPlayer() {
    currentPlayer = currentPlayer === 1 ? 2 : 1;
}
function initPlayAI(color) {
    startNewGame()
    isplayingWithAI = true;
    if (color === "black") {
        setTimeout(function () {
            
            handleMove("AIMove");
        
        }, 500);
    }
}
function initPlayOffline() {
    startNewGame();
    isplayingWithAI = false;
    startTimers(); 
    // Add other function calls as needed
}

function rotateBoard() {
    /*
    *  TODO: Fill the rotation function to rotate after each move.
    *   Also rotate if player is black when playing versus AI.
    */
}


