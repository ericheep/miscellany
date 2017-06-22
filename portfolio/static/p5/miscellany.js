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

function Diamond(originX, originY, size) {
    this.p1 = createVector(-size, -size);
    this.p2 = createVector(-size,  size);
    this.p3 = createVector( size,  size);
    this.p4 = createVector( size, -size);

    this.v1 = createVector(-size, -size);
    this.v2 = createVector(-size,  size);
    this.v3 = createVector( size,  size);
    this.v4 = createVector( size, -size);

    this.travel = function() {

    };

    this.display = function() {
        stroke(255, 220, 220);
        translate(originX, originY)

        beginShape();
        vertex(this.v1.x, this.v1.y);
        vertex(this.v2.x, this.v2.y);
        vertex(this.v3.x, this.v3.y);
        vertex(this.v4.x, this.v4.y);
        vertex(this.v5.x, this.v5.y);
        endShape();
    };
}
