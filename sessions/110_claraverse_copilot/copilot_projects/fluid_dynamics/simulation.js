// Lattice Boltzmann Method (D2Q9) Fluid Simulation

class FluidSimulation {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Simulation parameters
        this.width = 500;
        this.height = 200;
        this.scale = 3; // Scale factor for rendering
        
        // Set canvas size
        this.canvas.width = this.width * this.scale;
        this.canvas.height = this.height * this.scale;
        
        // LBM parameters
        this.viscosity = 0.02;
        this.omega = 1.0 / (3.0 * this.viscosity + 0.5);
        this.inflowSpeed = 0.08;
        
        // D2Q9 lattice velocities
        this.ex = [0, 1, 0, -1, 0, 1, -1, -1, 1];
        this.ey = [0, 0, 1, 0, -1, 1, 1, -1, -1];
        this.weights = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36];
        
        // Obstacle parameters
        this.obstacle = {
            x: this.width / 3,
            y: this.height / 2,
            radius: 12,
            dragging: false
        };
        
        // Initialize arrays
        this.initArrays();
        
        // Mouse interaction
        this.setupMouseHandlers();
        
        // FPS tracking
        this.fps = 0;
        this.lastTime = performance.now();
        this.frameCount = 0;
        
        // Start simulation
        this.running = true;
        this.animate();
    }
    
    initArrays() {
        const size = this.width * this.height;
        
        // Distribution functions (9 directions)
        this.f = new Array(9).fill(0).map(() => new Float32Array(size));
        this.fNew = new Array(9).fill(0).map(() => new Float32Array(size));
        
        // Macroscopic variables
        this.density = new Float32Array(size);
        this.ux = new Float32Array(size);
        this.uy = new Float32Array(size);
        
        // Barrier array
        this.barrier = new Uint8Array(size);
        
        // Initialize with equilibrium
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = x + y * this.width;
                const rho = 1.0;
                const vx = this.inflowSpeed;
                const vy = 0.0;
                
                this.density[idx] = rho;
                this.ux[idx] = vx;
                this.uy[idx] = vy;
                
                // Set equilibrium distribution
                for (let i = 0; i < 9; i++) {
                    this.f[i][idx] = this.equilibrium(i, rho, vx, vy);
                }
            }
        }
        
        this.updateBarrier();
    }
    
    equilibrium(i, rho, vx, vy) {
        const eu = this.ex[i] * vx + this.ey[i] * vy;
        const uv = vx * vx + vy * vy;
        return this.weights[i] * rho * (1.0 + 3.0 * eu + 4.5 * eu * eu - 1.5 * uv);
    }
    
    updateBarrier() {
        // Clear barrier
        this.barrier.fill(0);
        
        // Set top and bottom walls
        for (let x = 0; x < this.width; x++) {
            this.barrier[x] = 1;
            this.barrier[x + (this.height - 1) * this.width] = 1;
        }
        
        // Set cow-shaped obstacle
        const ox = Math.round(this.obstacle.x);
        const oy = Math.round(this.obstacle.y);
        const scale = this.obstacle.radius / 12; // Scale based on original radius
        
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.isInsideCow(x - ox, y - oy, scale)) {
                    this.barrier[x + y * this.width] = 1;
                }
            }
        }
    }
    
    isInsideCow(dx, dy, scale) {
        // Cow body (large ellipse)
        const bodyX = dx / (14 * scale);
        const bodyY = dy / (10 * scale);
        if (bodyX * bodyX + bodyY * bodyY < 1) return true;
        
        // Cow head (circle)
        const headDx = dx - 16 * scale;
        const headDy = dy;
        const headR = 7 * scale;
        if (headDx * headDx + headDy * headDy < headR * headR) return true;
        
        // Cow snout (small ellipse)
        const snoutDx = (dx - 21 * scale) / (3 * scale);
        const snoutDy = dy / (2.5 * scale);
        if (snoutDx * snoutDx + snoutDy * snoutDy < 1) return true;
        
        // Ears (two small circles)
        const ear1Dx = dx - 14 * scale;
        const ear1Dy = dy - 8 * scale;
        const earR = 2.5 * scale;
        if (ear1Dx * ear1Dx + ear1Dy * ear1Dy < earR * earR) return true;
        
        const ear2Dx = dx - 14 * scale;
        const ear2Dy = dy + 8 * scale;
        if (ear2Dx * ear2Dx + ear2Dy * ear2Dy < earR * earR) return true;
        
        // Four legs
        const legWidth = 3 * scale;
        const legHeight = 8 * scale;
        
        // Front left leg
        if (Math.abs(dx - 8 * scale) < legWidth && dy > 8 * scale && dy < 8 * scale + legHeight) return true;
        // Front right leg
        if (Math.abs(dx - 8 * scale) < legWidth && dy < -8 * scale && dy > -8 * scale - legHeight) return true;
        // Back left leg
        if (Math.abs(dx + 8 * scale) < legWidth && dy > 8 * scale && dy < 8 * scale + legHeight) return true;
        // Back right leg
        if (Math.abs(dx + 8 * scale) < legWidth && dy < -8 * scale && dy > -8 * scale - legHeight) return true;
        
        return false;
    }
    
    collide() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = x + y * this.width;
                
                if (this.barrier[idx]) continue;
                
                // Compute macroscopic variables
                let rho = 0;
                let vx = 0;
                let vy = 0;
                
                for (let i = 0; i < 9; i++) {
                    rho += this.f[i][idx];
                    vx += this.ex[i] * this.f[i][idx];
                    vy += this.ey[i] * this.f[i][idx];
                }
                
                vx /= rho;
                vy /= rho;
                
                this.density[idx] = rho;
                this.ux[idx] = vx;
                this.uy[idx] = vy;
                
                // Collision (BGK)
                for (let i = 0; i < 9; i++) {
                    const feq = this.equilibrium(i, rho, vx, vy);
                    this.f[i][idx] += this.omega * (feq - this.f[i][idx]);
                }
            }
        }
    }
    
    stream() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = x + y * this.width;
                
                for (let i = 0; i < 9; i++) {
                    const nx = x - this.ex[i];
                    const ny = y - this.ey[i];
                    
                    if (nx >= 0 && nx < this.width && ny >= 0 && ny < this.height) {
                        const nidx = nx + ny * this.width;
                        this.fNew[i][idx] = this.f[i][nidx];
                    } else {
                        this.fNew[i][idx] = this.f[i][idx];
                    }
                }
            }
        }
        
        // Swap arrays
        [this.f, this.fNew] = [this.fNew, this.f];
    }
    
    bounce() {
        // Bounce-back boundary condition for barriers
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = x + y * this.width;
                
                if (this.barrier[idx]) {
                    // Swap opposite directions
                    [this.f[1][idx], this.f[3][idx]] = [this.f[3][idx], this.f[1][idx]];
                    [this.f[2][idx], this.f[4][idx]] = [this.f[4][idx], this.f[2][idx]];
                    [this.f[5][idx], this.f[7][idx]] = [this.f[7][idx], this.f[5][idx]];
                    [this.f[6][idx], this.f[8][idx]] = [this.f[8][idx], this.f[6][idx]];
                }
            }
        }
    }
    
    applyBoundaryConditions() {
        // Left boundary (inflow)
        for (let y = 1; y < this.height - 1; y++) {
            const idx = 0 + y * this.width;
            const rho = 1.0;
            const vx = this.inflowSpeed;
            const vy = 0.0;
            
            for (let i = 0; i < 9; i++) {
                this.f[i][idx] = this.equilibrium(i, rho, vx, vy);
            }
        }
        
        // Right boundary (outflow) - simple extrapolation
        for (let y = 1; y < this.height - 1; y++) {
            const idx = (this.width - 1) + y * this.width;
            const idx2 = (this.width - 2) + y * this.width;
            
            for (let i = 0; i < 9; i++) {
                this.f[i][idx] = this.f[i][idx2];
            }
        }
    }
    
    step() {
        this.collide();
        this.stream();
        this.bounce();
        this.applyBoundaryConditions();
    }
    
    render() {
        const imageData = this.ctx.createImageData(this.width, this.height);
        const data = imageData.data;
        
        // Color based on velocity magnitude
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = x + y * this.width;
                const pixelIdx = (x + y * this.width) * 4;
                
                if (this.barrier[idx]) {
                    // Obstacle color
                    data[pixelIdx] = 80;
                    data[pixelIdx + 1] = 80;
                    data[pixelIdx + 2] = 80;
                    data[pixelIdx + 3] = 255;
                } else {
                    // Velocity magnitude
                    const speed = Math.sqrt(this.ux[idx] * this.ux[idx] + this.uy[idx] * this.uy[idx]);
                    const curl = this.computeCurl(x, y);
                    
                    // Use curl for coloring (vorticity visualization)
                    const colorValue = Math.abs(curl) * 500;
                    
                    // RGB color mapping
                    const hue = 240 - Math.min(colorValue * 240, 240); // Blue to red
                    const rgb = this.hslToRgb(hue / 360, 1.0, 0.5);
                    
                    data[pixelIdx] = rgb[0];
                    data[pixelIdx + 1] = rgb[1];
                    data[pixelIdx + 2] = rgb[2];
                    data[pixelIdx + 3] = 255;
                }
            }
        }
        
        // Create temporary canvas at original size
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = this.width;
        tempCanvas.height = this.height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.putImageData(imageData, 0, 0);
        
        // Scale up to display size
        this.ctx.imageSmoothingEnabled = false;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(tempCanvas, 0, 0, this.canvas.width, this.canvas.height);
    }
    
    computeCurl(x, y) {
        if (x <= 0 || x >= this.width - 1 || y <= 0 || y >= this.height - 1) {
            return 0;
        }
        
        const idx = x + y * this.width;
        const idxRight = (x + 1) + y * this.width;
        const idxLeft = (x - 1) + y * this.width;
        const idxUp = x + (y - 1) * this.width;
        const idxDown = x + (y + 1) * this.width;
        
        const dudy = (this.ux[idxUp] - this.ux[idxDown]) * 0.5;
        const dvdx = (this.uy[idxRight] - this.uy[idxLeft]) * 0.5;
        
        return dvdx - dudy;
    }
    
    hslToRgb(h, s, l) {
        let r, g, b;
        
        if (s === 0) {
            r = g = b = l;
        } else {
            const hue2rgb = (p, q, t) => {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1/6) return p + (q - p) * 6 * t;
                if (t < 1/2) return q;
                if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            };
            
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }
        
        return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
    }
    
    animate() {
        if (!this.running) return;
        
        // Run multiple simulation steps per frame for speed
        for (let i = 0; i < 8; i++) {
            this.step();
        }
        
        this.render();
        
        // FPS calculation
        this.frameCount++;
        const currentTime = performance.now();
        if (currentTime - this.lastTime >= 1000) {
            this.fps = this.frameCount;
            this.frameCount = 0;
            this.lastTime = currentTime;
            document.getElementById('fps').textContent = this.fps;
        }
        
        requestAnimationFrame(() => this.animate());
    }
    
    setupMouseHandlers() {
        let mouseDown = false;
        let lastMouseX = 0;
        let lastMouseY = 0;
        
        const getMousePos = (e) => {
            const rect = this.canvas.getBoundingClientRect();
            return {
                x: (e.clientX - rect.left) / this.scale,
                y: (e.clientY - rect.top) / this.scale
            };
        };
        
        this.canvas.addEventListener('mousedown', (e) => {
            const pos = getMousePos(e);
            const dx = pos.x - this.obstacle.x;
            const dy = pos.y - this.obstacle.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist <= this.obstacle.radius) {
                mouseDown = true;
                this.obstacle.dragging = true;
                lastMouseX = pos.x;
                lastMouseY = pos.y;
            }
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (mouseDown && this.obstacle.dragging) {
                const pos = getMousePos(e);
                this.obstacle.x = Math.max(this.obstacle.radius, Math.min(this.width - this.obstacle.radius, pos.x));
                this.obstacle.y = Math.max(this.obstacle.radius, Math.min(this.height - this.obstacle.radius, pos.y));
                this.updateBarrier();
            }
        });
        
        this.canvas.addEventListener('mouseup', () => {
            mouseDown = false;
            this.obstacle.dragging = false;
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            mouseDown = false;
            this.obstacle.dragging = false;
        });
        
        // Touch support for mobile
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            const mouseEvent = new MouseEvent('mousedown', {
                clientX: touch.clientX,
                clientY: touch.clientY
            });
            this.canvas.dispatchEvent(mouseEvent);
        });
        
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            const mouseEvent = new MouseEvent('mousemove', {
                clientX: touch.clientX,
                clientY: touch.clientY
            });
            this.canvas.dispatchEvent(mouseEvent);
        });
        
        this.canvas.addEventListener('touchend', (e) => {
            e.preventDefault();
            const mouseEvent = new MouseEvent('mouseup', {});
            this.canvas.dispatchEvent(mouseEvent);
        });
    }
    
    setViscosity(value) {
        this.viscosity = value;
        this.omega = 1.0 / (3.0 * this.viscosity + 0.5);
    }
    
    setInflowSpeed(value) {
        this.inflowSpeed = value;
    }
    
    resetObstacle() {
        this.obstacle.x = this.width / 3;
        this.obstacle.y = this.height / 2;
        this.updateBarrier();
    }
}

// Initialize simulation when page loads
window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    const simulation = new FluidSimulation(canvas);
    
    // Control handlers
    const viscositySlider = document.getElementById('viscosity');
    const viscosityValue = document.getElementById('viscosity-value');
    const speedSlider = document.getElementById('speed');
    const speedValue = document.getElementById('speed-value');
    const resetButton = document.getElementById('reset');
    
    viscositySlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        viscosityValue.textContent = value.toFixed(2);
        simulation.setViscosity(value);
    });
    
    speedSlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        speedValue.textContent = value.toFixed(2);
        simulation.setInflowSpeed(value);
    });
    
    resetButton.addEventListener('click', () => {
        simulation.resetObstacle();
    });
});
