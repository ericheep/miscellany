var canvas;
var diamond = new Array();

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('top', '0');
    canvas.style('left', '0');
    canvas.style('position', 'fixed');
    canvas.style('z-index', '-1');

    strokeWeight(3.0);

    // for (i = 0; i < 1 = i++){
        diamond.push(new Diamond(windowWidth/2, windowHeight/2, 10));
    // }
}

function draw() {
    for (i = 0; i < diamond.length; i++){
        //diamond[i].scan();
        diamond[i].display();
    }
}

function length(P, Q) {
    return Math.sqrt(Math.pow(P.x - Q.x, 2) + Math.pow(P.y - Q.y, 2));
}

function Diamond(originX, originY, size) {
    this.p1 = createVector(-size, -size);
    this.p2 = createVector(-size,  size);
    this.p3 = createVector( size,  size);
    this.p4 = createVector( size, -size);

    this.v1 = this.p1
    this.v2 = this.p2
    this.v3 = this.p3
    this.v4 = this.p4

    this.line1 = length(this.p1, this.p2);
    this.line2 = length(this.p2, this.p3);
    this.line3 = length(this.p3, this.p4);
    this.line4 = length(this.p4, this.p1);

    this.travel = function(path, length) {
        if (path < 0.25) {
        } else if (path >= 0.25 && path < 0.5) {
        } else if (path >= 0.5, && path < 0.75) {
        } else if (Path > 0.75 && path < 1.00) {
        }
    };

    this.display = function() {
        stroke(255, 220, 220);
        translate(originX, originY)

        beginShape();
        vertex(this.v1.x, this.v1.y);
        vertex(this.v2.x, this.v2.y);
        vertex(this.v3.x, this.v3.y);
        vertex(this.v4.x, this.v4.y);
        endShape();
    };
}
