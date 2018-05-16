const Enemy = function(x, y, w, h, col, s, he) {
  this.alive = true;
  this.x = x;
  this.y = y;
  this.vel = s;
  this.w = w;
  this.h = h;
  this.ang = 0;
  this.col = col;
  this.health = he;
};

Enemy.prototype.update = function() {
  this.ang = angle(this.x, this.y, tank.x, tank.y) - PI/2;

  // forward / back vel
  this.x += this.vel * sin(-this.ang);
  this.y += this.vel * cos(this.ang);

  tank.bs.forEach((b) => {
    if (this.hit(b.x, b.y)) {
      b.alive = false;
      this.alive = false;
    }
  });
};

Enemy.prototype.show = function() {
  this.update();

  push();
  noStroke();
  translate(this.x, this.y);
  rotate(this.ang);
  fill(this.col);
  beginShape();
  vertex(-this.w/2, -this.h/2);
  vertex(0, this.h/2);
  vertex(this.w/2, -this.h/2);
  endShape(CLOSE);
  pop();
};

Enemy.prototype.hit = function(x,y) {
  let hw = this.w / 2;
  let hh = this.h / 2;
  return x >= this.x - hw && x <= this.x + hw && y >= this.y - hh && y <= this.y + hh
}