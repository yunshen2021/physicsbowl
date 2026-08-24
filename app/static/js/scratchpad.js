class PhysicsScratchpad {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.isDrawing = false;
    this.color = "#58a6ff";
    this.lineWidth = 2;
    this.isEraser = false;

    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());

    this.setupEvents();
  }

  resizeCanvas() {
    if (!this.canvas) return;
    const parent = this.canvas.parentElement;
    this.canvas.width = parent.clientWidth || 400;
    this.canvas.height = parent.clientHeight || 260;
    this.ctx.fillStyle = "#0d1117";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  setupEvents() {
    const getPos = (e) => {
      const rect = this.canvas.getBoundingClientRect();
      return {
        x: (e.clientX || e.touches[0].clientX) - rect.left,
        y: (e.clientY || e.touches[0].clientY) - rect.top
      };
    };

    const start = (e) => {
      e.preventDefault();
      this.isDrawing = true;
      const pos = getPos(e);
      this.ctx.beginPath();
      this.ctx.moveTo(pos.x, pos.y);
    };

    const move = (e) => {
      if (!this.isDrawing) return;
      e.preventDefault();
      const pos = getPos(e);
      this.ctx.lineTo(pos.x, pos.y);
      this.ctx.strokeStyle = this.isEraser ? "#0d1117" : this.color;
      this.ctx.lineWidth = this.isEraser ? 16 : this.lineWidth;
      this.ctx.lineCap = "round";
      this.ctx.lineJoin = "round";
      this.ctx.stroke();
    };

    const stop = () => {
      this.isDrawing = false;
    };

    this.canvas.addEventListener("mousedown", start);
    this.canvas.addEventListener("mousemove", move);
    this.canvas.addEventListener("mouseup", stop);
    this.canvas.addEventListener("mouseleave", stop);

    this.canvas.addEventListener("touchstart", start);
    this.canvas.addEventListener("touchmove", move);
    this.canvas.addEventListener("touchend", stop);
  }

  setColor(c) {
    this.color = c;
    this.isEraser = false;
  }

  setEraser() {
    this.isEraser = true;
  }

  clear() {
    if (!this.canvas) return;
    this.ctx.fillStyle = "#0d1117";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }
}

let activeScratchpad = null;
function initScratchpad() {
  if (!activeScratchpad) {
    activeScratchpad = new PhysicsScratchpad("scratchpad-canvas");
  }
}
