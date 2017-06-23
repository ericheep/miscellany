var canvas;
var tracer = new Array();
var x = new Array();
var y = new Array();

var numTracers = 2;
var numPoints = 4;

var inc = 0.0;

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('top', '0');
    canvas.style('left', '0');
    canvas.style('position', 'fixed');
    canvas.style('z-index', '-1');

    // strokeWeight(3.0);

    for (var i = 0; i < numTracers; i++) {
        for (var j = 0; j < numPoints; j++) {
            x.push(random(width));
            y.push(random(height));
        }
        tracer.push(new Tracer(numPoints, x, y));
    };
}

function draw() {
    background(100);
    inc = (inc + 1.0/(30.0 * 16.0)) % 1.0;
    /*for (i = 0; i < numTracers; i++){
          tracer[i].trace((inc + i * 0.01) % 1.0, 0.5);
    }*/
}

function Tracer(numPoints) {
    var invNumPoints(1.0/numPoints);
    var range;

    this.p = new Array();
    this.v = createVector(0.0, 0.0);
    this.d = createVector(0.0, 0.0);

    for (var i = 0; i < numPoints; i++) {
        this.p.push(createVector(x[i], y[i]));
    };

    this.drawVertex = function(pos, idx) {
        where = (idx + 1) * invNumPoints;

    };

    this.trace = function(path, length) {

    };
};
