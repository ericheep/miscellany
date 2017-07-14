var canvas;
var tracer = new Array();

var inc = 0.0;
var speed = 0.0;
var numPoints = 0;
var numTracers = 0;
var numDots = 0;

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

    speed = 0.000125
    numPoints = int(random(4, 8));
    numTracers = int(random(1000, 2000));

    var x = []
    var y = []

    for (var i = 0; i < numPoints; i++) {
        x.push(random(windowWidth));
        y.push(random(windowHeight));
    };

    for (var j = 0; j < numTracers; j++) {
        tracer.push(new Tracer(numPoints, numDots, x, y, 0.5));
    }
}

function draw() {
    background(255);
    inc = (inc + speed) % 1.0;

    for (var i = 0; i < numTracers; i++) {
        tracer[i].trace((inc + i * 0.01) % 1.0, 0.5);
    }
}

function Tracer(numPoints, numDots, x, y, len) {
    var invNumPoints = 1.0/numPoints;
    var invNumDots = 1.0/numDots;

    this.p = new Array();

    for (var i = 0; i < numPoints; i++) {
        this.p.push(createVector(x[i], y[i]));
    };

    var range;
    var where;

    this.v = createVector(0.0, 0.0);
    this.d = createVector(0.0, 0.0);

    this.trace = function(pos) {
        for (var i = 0; i < numPoints; i++) {
            var where = (i + 1) * invNumPoints;

            if (pos < where) {
                this.v.set(this.p[(i + 1) % numPoints].x, this.p[(i + 1) % numPoints].y);
                this.d = this.v.copy().sub(createVector(this.p[i].x, this.p[i].y));

                this.d.x = this.d.x * (pos - where) * numPoints;
                this.d.y = this.d.y * (pos - where) * numPoints;
                this.v.add(this.d);

                fill(255, 0, 0);
                stroke(255, 0, 0);
                ellipse(this.v.x, this.v.y, 2, 2);
                break;
            };
        };
    };
};
