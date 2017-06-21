var canvas;
var creeper = new Array();

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('top', '0');
    canvas.style('left', '0');
    canvas.style('position', 'fixed');
    canvas.style('z-index', '-1');

    for (i = 0; i < windowHeight; i++){
        creeper.push(new Creeper(0, i));
    }
}

function draw() {
    for (i = 0; i < windowHeight; i++){
        creeper[i].creep();
        creeper[i].display();
    }
}

function Creeper(x, y) {
    this.x1 = x;
    this.y1 = y;

    this.x2 = x;
    this.y2 = y;

    this.creep = function() {
        this.x2 += Math.floor((Math.random() * 5) + 1);
    };

    this.display = function() {
        stroke(250, 250, 250);
        line(this.x1, this.y1, this.x2, this.y2);
    }
}
