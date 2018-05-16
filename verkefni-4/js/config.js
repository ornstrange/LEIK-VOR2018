// keys
const W = 87;
const A = 65;
const S = 83;
const D = 68;
const SPACE = 32;

// colors
const BACKGROUND = "#fceadd";

// TANK SETTINGS
const TANKW = 3.5;
const TANKH = 6.5;
const TANKMSPEED = 4.4;
const TANKRSPEED = 0.042;

// BULLET SETTINGS
const BSPEED = 50;
const BDAMP = 0.03;
const BTHRESH = 20;

// helpers
function angle(cx, cy, ex, ey) {
  // gráða frá miðjupunkt til endapunkts
  var dx = ex - cx;
  var dy = ey - cy;
  var theta = Math.atan2(dy, dx);
  return theta;
};

const Percent = function() {
  this.mWidth = windowWidth;
  this.mHeight = windowHeight;
  if (this.mWidth >= 1920) {
    this.mWidth = 1920;
  };
  if (this.mHeight >= 1080) {
    this.mHeight = 1080;
  };
  this.x = function(numb) {
    return Math.ceil(numb / 100 * this.mWidth);
  };
  this.y = function(numb) {
    return Math.ceil(numb / 100 * this.mHeight);
  };
};