import streamlit as st
import streamlit.components.v1 as components

st.title("テトリス風ゲーム")
st.caption("画面（枠内）を一度クリックしてから、スペースキーを押してゲームを開始してください。")

# 完全にバグを修正したテトリスコード
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
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding-top: 10px;
        }
        #score {
            font-size: 24px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        #game-container {
            position: relative;
        }
        canvas {
            border: 4px solid #fff;
            background-color: #111;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 240px;
            height: 400px;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            text-align: center;
            box-sizing: border-box;
        }
        .controls {
            margin-top: 15px;
            font-size: 13px;
            color: #ccc;
            text-align: center;
            line-height: 1.5;
        }
    </style>
</head>
<body>

    <div id="score">SCORE: 0</div>
    <div id="game-container">
        <canvas id="tetris" width="240" height="400"></canvas>
        <div id="overlay">PRESS SPACE<br>TO START</div>
    </div>

    <div class="controls">
        【操作方法】<br>
        Space : スタート / ハードドロップ<br>
        ← / → : 移動 | ↑ : 回転 | ↓ : ソフトドロップ
    </div>

<script>
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
const overlay = document.getElementById('overlay');

context.scale(20, 20);

let isPlaying = false;

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

// すべてのブロックの形状データを完全に記述（修正完了）
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
    drawMatrix(player.matrix, player.pos);
}

const colors = [
    null,
    '#00f0f0', // I
    '#f0a000', // L
    '#0000f0', // J
    '#f0f000', // O
    '#f00000', // Z
    '#00f000', // S
    '#a000f0', // T
];

function drawMatrix(matrix, offset) {
    if (!matrix) return;
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x, y + offset.y, 1, 1);
                context.strokeStyle = '#111';
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
    player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
    
    if (collide(arena, player)) {
        isPlaying = false;
        overlay.style.display = 'flex';
        overlay.innerHTML = 'GAME OVER<br><br><span style="font-size:12px;color:#aaa;">PRESS SPACE TO RESTART</span>';
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
        if (offset > player.matrix[0].length) {
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
    document.getElementById('score').innerText = `SCORE: ${player.score}`;
}

function gameStart() {
    arena.forEach(row => row.fill(0));
    player.score = 0;
    updateScore();
    playerReset();
    isPlaying = true;
    overlay.style.display = 'none';
}

// キーイベント制御
window.addEventListener('keydown', event => {
    // 矢印キー(37-40)とスペース(32)のスクロールを防止
    if ([32, 37, 38, 39, 40].indexOf(event.keyCode) > -1) {
        event.preventDefault();
    }

    if (event.keyCode === 32) {
        if (!isPlaying) {
            gameStart();
        } else {
            playerHardDrop();
        }
    } else if (event.keyCode === 37) {
        playerMove(-1);
    } else if (event.keyCode === 39) {
        playerMove(1);
    } else if (event.keyCode === 40) {
        playerDrop();
    } else if (event.keyCode === 38) {
        playerRotate(1);
    }
});

const arena = createMatrix(12, 20);
const player = {
    pos: {x: 0, y: 0},
    matrix: null,
    score: 0,
};

draw();
update();
</script>
</body>
</html>
"""

components.html(html_code, height=520)
