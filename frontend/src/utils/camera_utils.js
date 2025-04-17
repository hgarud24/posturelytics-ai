// https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js
export class Camera {
    constructor(videoElement, options) {
      this.video = videoElement;
      this.onFrame = options.onFrame;
      this.width = options.width;
      this.height = options.height;
      this.video.width = this.width;
      this.video.height = this.height;
      this.video.style.objectFit = 'cover';
    }
  
    async start() {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: this.width, height: this.height }
      });
  
      this.video.srcObject = stream;
  
      await new Promise((resolve) => {
        this.video.onloadedmetadata = () => {
          resolve();
        };
      });
  
      this.video.play();
      this._process();
    }
  
    async _process() {
      if (this.video.paused || this.video.ended) return;
  
      await this.onFrame();
  
      requestAnimationFrame(this._process.bind(this));
    }
  }
  