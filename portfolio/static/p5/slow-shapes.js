var canvas;
var tracer = new Array();

var inc = 0.0;
var speed = 0.0;
var numPoints = 0;
var numTracers = 0;

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('top', '0');
    canvas.style('left', '0');
    canvas.style('position', 'fixed');
    canvas.style('z-index', '-1');

    strokeWeight(0.1);

    speed = 0.00005
    numPoints = int(random(4, 8));
    numTracers = int(random(2, 5));

    for (var j = 0; j < numTracers; j++) {
        var x = []
        var y = []

        for (var i = 0; i < numPoints; i++) {
            x.push(random(windowWidth));
            y.push(random(windowHeight));

        };
        tracer.push(new Tracer(numPoints, x, y, random(0.1, 0.5)));
    }
}

function draw() {
    background(255);
    inc = (inc + speed) % 1.0;

    stroke(255, 0, 0);
    fill(150, 150, 150, 5);
    for (var i = 0; i < numTracers; i++) {
        tracer[i].trace(inc % 1.0, 0.5);
    }
}

function Tracer(numPoints, x, y, len) {
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

    this.trace = function(pos) {
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
