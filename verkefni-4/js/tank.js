const Tank = function(x, y, w, h, col, tcol, bcol, ccol) {
  this.x = x;
  this.y = y;
  this.vel = 0;
  this.avel = 0;
  this.w = w;
  this.h = h;
  this.ang = 0;
  this.gang = 0;
  this.col = col;
  this.tcol = tcol;
  this.bcol = bcol;
  this.ccol = ccol;
  this.bs = [];
  this.blim = 10;
  this.health = 100;
};

Tank.prototype.actions = function() {
  // forward backwards
  if (keyIsDown(W)) {
    this.vel = -TANKMSPEED;
  } else if (keyIsDown(S)) {
    this.vel = TANKMSPEED;
  } else {
    this.vel = 0;
  }

  // rotation
  if (keyIsDown(A)) {
    this.avel = -TANKRSPEED;
  } else if (keyIsDown(D)) {
    this.avel = TANKRSPEED;
  } else {
    this.avel = 0;
  }
}

Tank.prototype.update = function() {
  this.actions(); // actions

  this.ang += this.avel // angular vel
  this.gang = angle(this.x, this.y, mouseX, mouseY) + PI / 2;

  // forward / back vel
  this.x += this.vel * sin(-this.ang);
  this.y += this.vel * cos(this.ang);

  // remove bullets
  this.bs = this.bs.filter(b => b.alive);
};

Tank.prototype.showTreads = function() {
  fill(this.tcol);
  rect(-this.w / 2, 0, this.w * 0.3, this.h * 0.85);
  rect(this.w / 2, 0, this.w * 0.3, this.h * 0.85);
  for (let i = -0.3; i < 0.4; i += 0.1) {
    rect(-this.w * 0.64, this.h * i, this.w * 0.1, this.h * 0.05, this.h * 0.1);
    rect(this.w * 0.64, this.h * i, this.w * 0.1, this.h * 0.05, this.h * 0.1);
  }
  rect(-this.w * 0.25, this.h * 0.55, this.w * 0.1, this.h * 0.15, this.h * 0.1);
  rect(this.w * 0.25, this.h * 0.55, this.w * 0.1, this.h * 0.15, this.h * 0.1);
};

Tank.prototype.showBody = function() {
  fill(this.col);
  rect(0, 0, this.w, this.h);
  ellipse(0, -this.h / 2, this.w, this.h * 0.1);
  ellipse(0, this.h / 2, this.w, this.h * 0.1);
};

Tank.prototype.showFrontGuard = function() {
  fill(this.tcol);
  for (let i = -0.25; i <= 0.25; i += 0.25) {
    ellipse(-this.w * i, -this.h * 0.46, this.w * 0.15, this.h * 0.08);
  }
}

Tank.prototype.showCanBase = function() {
  fill(this.bcol);
  rect(0, 0, this.w * 0.6, this.h * 0.4, this.h * 0.1);
};

Tank.prototype.showCannon = function() {
  fill(this.ccol);
  rect(0, -this.h * 0.35, this.w * 0.14, this.h * 0.7, this.w * 0.07)
};

Tank.prototype.show = function() {
  this.update();

  push();
  noStroke();
  translate(this.x, this.y);
  rotate(this.ang);
  this.showTreads();
  this.showBody();
  this.showFrontGuard();
  pop();

  this.bs.forEach(b => b.show());

  push();
  noStroke();
  translate(this.x, this.y);
  rotate(this.gang);
  this.showCanBase();
  this.showCannon();
  pop();
};

Tank.prototype.fire = function() {
  if (this.bs.length < this.blim) {
    this.bs.push(new Bullet(this.x, this.y, this.gang, this.w * 0.14))
  }
};

// BULLET
const Bullet = function(x, y, gang, s) {
  this.alive = true;
  this.x = x;
  this.y = y;
  this.v = BSPEED;
  this.d = 1 - BDAMP;
  this.a = gang;
  this.s = s;
};

Bullet.prototype.update = function() {
  this.v *= this.d; // DAMP

  // ANGLE
  this.x += this.v * sin(this.a);
  this.y += -this.v * cos(this.a);

  // KILL
  if (this.v <= BTHRESH) {
    this.alive = false;
  }

  // console.log('thresh: ' + BTHRESH);
  // console.log('damp: ' + this.d);
  // console.log('vel: ' + this.v);
};

Bullet.prototype.show = function() {
  this.update();

  push();
  noStroke();
  fill(0);
  translate(this.x, this.y);
  rotate(this.a);
  ellipse(0, 0, this.s, this.s);
  pop();
};