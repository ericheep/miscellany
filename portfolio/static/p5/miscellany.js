var canvas;
var tracer = new Array();

var numPoints = 4;

var inc = 0.0;
var rows = 0;
var cols = 0;
var cubeSize = 100;

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('top', '0');
    canvas.style('left', '0');
    canvas.style('position', 'fixed');
    canvas.style('z-index', '-1');

    strokeWeight(2.0);

    rows = int(windowWidth/cubeSize) + 1;
    cols = int(windowHeight/cubeSize) + 1;

    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            x = [i * cubeSize, (i + 1) * cubeSize, (i + 1) * cubeSize,       i * cubeSize];
            y = [j * cubeSize,       j * cubeSize, (j + 1) * cubeSize, (j + 1) * cubeSize];


            tracer.push(new Tracer(numPoints, x, y));
        }
    };
}

function draw() {
    background(255);
    inc = (inc + 1.0/(30.0 * 16.0)) % 1.0;
    stroke(255, 200, 200);
    for (i = 0; i < rows * cols; i++){
        // translate(windowWidth/2, windowHeight/2);
        // tracer[i].trace(((inc * 0.01 * float(i)/1.0)) % 1.0, 0.5);
        /*push();
        for (j = 0; j < rows; j++) {
            scale(0.9);
            tracer[i].trace((inc + i * 0.01) % 1.0, 0.5);
        }
        pop();*/
    }
}

function Tracer(numPoints, x, y) {
    var invNumPoints = 1.0/numPoints;

    this.p = new Array();

    for (var i = 0; i < numPoints; i++) {
        this.p.push(createVector(x[i], y[i]));
    };

    var range;
    var where;

    this.v = createVector(0.0, 0.0);
    this.d = createVector(0.0, 0.0);

    this.drawVertex = function(pos, idx) {
        where = (idx + 1) * invNumPoints;

        this.v.set(this.p[(idx + 1) % numPoints].x, this.p[(idx + 1) % numPoints].y);
        this.d = this.v.copy().sub(this.p[idx]);

        this.d.x = this.d.x * (pos - where) * numPoints;
        this.d.y = this.d.y * (pos - where) * numPoints;
        this.v.add(this.d);

        vertex(this.v.x, this.v.y);
    };

    this.trace = function(pos, len) {
        var a = Math.floor(pos * numPoints);
        var b = Math.floor(((pos + len) * numPoints) % numPoints);

        range = b - a;
        if (a > b) {
            range = numPoints + range;
        }

        beginShape();
        this.drawVertex(pos, a);

        for (var i = a + 1; i < (a + range) + 1; i++) {
            vertex(this.p[i % numPoints].x, this.p[i % numPoints].y);
        }

        this.drawVertex((pos + len) % 1.0, b);
        endShape();
    };
};
