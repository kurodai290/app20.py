import streamlit as st
import streamlit.components.v1 as components

st.title("テトリス風ゲーム")
st.caption("画面（枠内）を一度クリックしてから、キーボードで操作してください。")

# 完全に動作するHTML/CSS/JSコード
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
        canvas {
            border: 4px solid #fff;
            background-color: #111;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
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
    <canvas id="tetris" width="240" height="400"></canvas>

    <div class="controls">
        【操作方法】<br>
        ← / → : 移動 | ↑ : 回転<br>
        ↓ : ソフトドロップ | Space : ハードドロップ
    </div>

<script>
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');

context.scale(20, 20);

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

// テトリミノの形状データを正しく定義
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
        arena.forEach(row => row.fill(0));
        player.score = 0;
        updateScore();
    }
}

function playerRotate(dir) {
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

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }

    draw();
    requestAnimationFrame(update);
}

function updateScore() {
    document.getElementById('score').innerText = `SCORE: ${player.score}`;
}

// キーイベント制御
window.addEventListener('keydown', event => {
    // 矢印キー(37-40)とスペース(32)のスクロールを防止
    if([32, 37, 38, 39, 40].indexOf(event.keyCode) > -1) {
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

playerReset();
updateScore();
update();
</script>
</body>
</html>
"""

components.html(html_code, height=520)
