// Örn Óli Strange
// 13.05.2018
var tank;
var ens = [];
var per;

// intro animation settings
var ts = 10;
var inc = 0.1;
var g = 1.022;

function setup() {
  p = new Percent();
  // canvas setup
  canvas = createCanvas(p.x(100), p.y(100));
  pixelDensity(1);

  rectMode(CENTER);

  tank = new Tank(width / 2, height / 2, p.x(TANKW), p.x(TANKH),
    "#37474f",
    "#263238",
    "#455a64",
    "#546e7a");
};

function update() {
	ens = ens.filter(e => e.alive);
};

function draw() {
	update();
  background(BACKGROUND);

  tank.show();
  ens.forEach(e => e.show());

  if (ts >= 1) {
    tank.w = p.x(TANKW) * ts;
    tank.h = p.x(TANKH) * ts;
    ts -= inc;
    inc *= g;
  } else {
    tank.w = p.x(TANKW);
    tank.h = p.x(TANKH);
    if (ens.length < 1  0) {
    	let rang = random() * PI * 2;
    	let newx = tank.x + (p.y(125) * sin(rang));
    	let newy = tank.y + (p.y(125) * cos(rang));
    	let spee = random(0.5, 2) * 3;
    	ens.push(new Enemy(newx, newy, p.x(4), p.x(3), "#f44336", spee, 50));
    }
  }
};

function keyPressed() {
  if (keyCode === SPACE) {
    tank.fire();
  }
  return false;
}

function mouseClicked() {
  tank.fire();
  return false;
}

function windowResized() {
  resizeCanvas(p.x(100), p.y(100));
};