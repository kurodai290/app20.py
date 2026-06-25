import streamlit as st
import streamlit.components.v1 as components

st.title("テトリス風ゲーム")
st.caption("START ボタンをクリックしてゲームを開始・リセットできます。")

# 構文エラーを完全に修正したテトリスコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background: #202023;
            color: #fff;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 10px;
            box-sizing: border-box;
        }
        #main-container {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 20px;
            background: #2d2d30;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        #game-area {
            position: relative;
        }
        canvas {
            border: 4px solid #444;
            background-color: #111;
            display: block;
        }
        #side-panel {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            width: 140px;
            height: 400px;
        }
        .panel-section {
            background: #1e1e1f;
            border: 2px solid #444;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 15px;
            text-align: center;
        }
        .panel-title {
            font-size: 12px;
            color: #aaa;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }
        #score-val {
            font-size: 24px;
            font-weight: bold;
            color: #00ffcc;
        }
        .btn {
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: bold;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        #start-btn {
            background: #28a745;
        }
        #reset-btn {
            background: #dc3545;
        }
        .controls-info {
            font-size: 11px;
            color: #bbb;
            line-height: 1.6;
            text-align: left;
            margin-top: auto;
        }
    </style>
</head>
<body>

    <div id="main-container">
        <div id="game-area">
            <canvas id="tetris" width="240" height="400"></canvas>
        </div>

        <div id="side-panel">
            <div class="panel-section">
                <div class="panel-title">SCORE</div>
                <div id="score-val">0</div>
            </div>

            <button id="start-btn" class="btn" onclick="pressStartButton()">START</button>
            <button id="reset-btn" class="btn" onclick="pressResetButton()">RESET</button>

            <div class="panel-section controls-info">
                <strong>【操作方法】</strong><br>
                ← / → : 左右移動<br>
                ↑ : ブロック回転<br>
                ↓ : 高速落下<br>
                Space : 即座に接地
            </div>
        </div>
    </div>

<script>
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
const scoreVal = document.getElementById('score-val');
const startBtn = document.getElementById('start-btn');

context.scale(20, 20);

let isPlaying = false;
let gameStartedOnce = false;

function arenaSweep() {
    let rowCount = 1;
    outer: for (let y = arena.length - 1; y > 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) {
                continue outer;
            }
        }
        const row = arena.splice(y, 1).fill(0);
        arena.unshift(row);
        ++y;

        player.score += rowCount * 10;
        rowCount *= 2;
    }
}

function collide(arena, player) {
    const [m, o] = [player.matrix, player.pos];
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
               (arena[y + o.y] &&
                arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

function createPiece(type) {
    if (type === 'I') {
        return [,
 ,
 ,
 ,
        ];
    } else if (type === 'L') {
        return [,
 ,
 ,
        ];
    } else if (type === 'J') {
        return [,
 ,
 ,
        ];
    } else if (type === 'O') {
        return [,
 ,
        ];
    } else if (type === 'Z') {
        return [,
 ,
 ,
        ];
    } else if (type === 'S') {
        return [,
 ,
 ,
        ];
    } else if (type === 'T') {
        return [,
 ,
 ,
        ];
    }
}

function draw() {
    context.fillStyle = '#111';
    context.fillRect(0, 0, canvas.width, canvas.height);

    drawMatrix(arena, {x: 0, y: 0});
    
    if (isPlaying) {
        drawMatrix(player.matrix, player.pos);
    }
}

const colors = [
    null,
    '#00f0f0',
    '#f0a000',
    '#0000f0',
    '#f0f000',
    '#f00000',
    '#00f0f0',
    '#a000f0',
];

function drawMatrix(matrix, offset) {
    if (!matrix) return;
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x, y + offset.y, 1, 1);
                context.strokeStyle = '#2d2d30';
                context.lineWidth = 0.05;
                context.strokeRect(x + offset.x, y + offset.y, 1, 1);
            }
        });
    });
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });
}

function playerDrop() {
    if (!isPlaying) return;
    player.pos.y++;
    if (collide(arena, player)) {
        player.pos.y--;
        merge(arena, player);
        playerReset();
        arenaSweep();
        updateScore();
    }
    dropCounter = 0;
}

function playerHardDrop() {
    if (!isPlaying) return;
    while (!collide(arena, player)) {
        player.pos.y++;
    }
    player.pos.y--;
    merge(arena, player);
    playerReset();
    arenaSweep();
    updateScore();
    dropCounter = 0;
}

function playerMove(offset) {
    if (!isPlaying) return;
    player.pos.x += offset;
    if (collide(arena, player)) {
        player.pos.x -= offset;
    }
}

function playerReset() {
    const pieces = 'TJLOSZI';
    player.matrix = createPiece(pieces[pieces.length * Math.random() | 0]);
    player.pos.y = 0;
    player.pos.x = (arena.length / 2 | 0) - (player.matrix.length / 2 | 0);
    
    if (collide(arena, player)) {
        isPlaying = false;
        startBtn.innerText = 'START';
        alert('GAME OVER! SCORE: ' + player.score);
    }
}

function playerRotate(dir) {
    if (!isPlaying) return;
    const pos = player.pos.x;
    let offset = 1;
    rotate(player.matrix, dir);
    while (collide(arena, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix.length) {
            rotate(player.matrix, -dir);
            player.pos.x = pos;
            return;
        }
    }
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
        }
    }
    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

let dropCounter = 0;
let dropInterval = 1000;
let lastTime = 0;

function update(time = 0) {
    const deltaTime = time - lastTime;
    lastTime = time;

    if (isPlaying) {
        dropCounter += deltaTime;
        if (dropCounter > dropInterval) {
            playerDrop();
        }
    }

    draw();
    requestAnimationFrame(update);
}

function updateScore() {
    scoreVal.innerText = player.score;
}

function pressStartButton() {
    if (!gameStartedOnce) {
        arena.forEach(row => row.fill(0));
        player.score = 0;
        updateScore();
        playerReset();
        gameStartedOnce = true;
    }
    
    if (isPlaying) {
        isPlaying = false;
        startBtn.innerText = 'START';
    } else {
        isPlaying = true;
        startBtn.innerText = 'PAUSE';
    }
}

function pressResetButton() {
    isPlaying = false;
    gameStartedOnce = false;
    arena.forEach(row => row.fill(0));
    player.score = 0;
    updateScore();
    startBtn.innerText = 'START';
    draw();
}

window.addEventListener('keydown', event => {
    if (!isPlaying) return;

    // スクロール防止用のキーコードリスト [32: Space, 37: Left, 38: Up, 39: Right, 40: Down]
    const keys =;
    if (keys.indexOf(event.keyCode) > -1) {
        event.preventDefault();
    }

    if (event.keyCode === 37) {
        playerMove(-1);
    } else if (event.keyCode === 39) {
        playerMove(1);
    } else if (event.keyCode === 40) {
        playerDrop();
    } else if (event.keyCode === 38) {
        playerRotate(1);
    } else if (event.keyCode === 32) {
        playerHardDrop();
    }
});

const arena = createMatrix(12, 20);
const player = {
    pos: {x: 0, y: 0},
    matrix: null,
    score: 0,
};

update();
</script>
</body>
</html>
"""

components.html(html_code, width=450, height=460)
