// Canvas setup
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Configuration
const config = {
    droneCount: 50,
    droneSize: 4,
    droneSpeed: 2,
    searchRadius: 15,
    gridSize: 5, // Smaller grid for better precision
    strategy: 'swarm', // Current search strategy
    // Swarm behavior parameters
    separationDistance: 30,
    alignmentDistance: 50,
    cohesionDistance: 50,
    separationWeight: 1.5,
    alignmentWeight: 1.0,
    cohesionWeight: 1.0,
    targetWeight: 2.0,
    maxSpeed: 3,
    maxForce: 0.1
};

// Statistics
const stats = {
    timeSteps: 0,
    clearTimes: [],
    currentAreaStartTime: null
};

// State
let drones = [];
let searchAreas = [];
let isDrawing = false;
let currentPath = [];

// Search Area class with optimized grid tracking
class SearchArea {
    constructor(path) {
        this.path = path;
        this.path2D = new Path2D();
        this.grid = new Map(); // Grid cells
        this.unsearchedCells = new Set(); // Fast lookup of unsearched cells
        this.totalCells = 0;
        this.createdAt = stats.timeSteps;
        this.clearedAt = null;
        this.wasComplete = false;
        
        this.initializePath();
        this.initializeGrid();
    }
    
    initializePath() {
        if (this.path.length === 0) return;
        
        this.path2D.moveTo(this.path[0].x, this.path[0].y);
        for (let i = 1; i < this.path.length; i++) {
            this.path2D.lineTo(this.path[i].x, this.path[i].y);
        }
        this.path2D.closePath();
    }
    
    initializeGrid() {
        // Get bounding box
        let minX = Infinity, minY = Infinity;
        let maxX = -Infinity, maxY = -Infinity;
        
        for (const p of this.path) {
            minX = Math.min(minX, p.x);
            minY = Math.min(minY, p.y);
            maxX = Math.max(maxX, p.x);
            maxY = Math.max(maxY, p.y);
        }
        
        // Sample multiple points per cell for better accuracy
        const samplePoints = 3; // Check 3x3 = 9 points per cell
        
        for (let x = Math.floor(minX / config.gridSize) * config.gridSize; x <= maxX; x += config.gridSize) {
            for (let y = Math.floor(minY / config.gridSize) * config.gridSize; y <= maxY; y += config.gridSize) {
                // Check if any sample point in the cell is inside the polygon
                let inside = false;
                
                for (let sx = 0; sx < samplePoints; sx++) {
                    for (let sy = 0; sy < samplePoints; sy++) {
                        const testX = x + (sx + 0.5) * (config.gridSize / samplePoints);
                        const testY = y + (sy + 0.5) * (config.gridSize / samplePoints);
                        
                        if (isPointInPolygon(testX, testY, this.path)) {
                            inside = true;
                            break;
                        }
                    }
                    if (inside) break;
                }
                
                if (inside) {
                    const gridX = Math.floor(x / config.gridSize);
                    const gridY = Math.floor(y / config.gridSize);
                    const key = `${gridX},${gridY}`;
                    
                    this.grid.set(key, {
                        x: x,
                        y: y,
                        centerX: x + config.gridSize / 2,
                        centerY: y + config.gridSize / 2,
                        searched: false
                    });
                    this.unsearchedCells.add(key);
                    this.totalCells++;
                }
            }
        }
    }
    
    markSearched(x, y, radius) {
        const gridX = Math.floor(x / config.gridSize);
        const gridY = Math.floor(y / config.gridSize);
        const radiusInCells = Math.ceil(radius / config.gridSize);
        
        for (let dx = -radiusInCells; dx <= radiusInCells; dx++) {
            for (let dy = -radiusInCells; dy <= radiusInCells; dy++) {
                const key = `${gridX + dx},${gridY + dy}`;
                const cell = this.grid.get(key);
                
                if (cell && !cell.searched) {
                    // Check if drone is close enough to cell center
                    const dist = Math.sqrt((x - cell.centerX) ** 2 + (y - cell.centerY) ** 2);
                    
                    // Mark as searched if drone is within radius of cell center
                    // Use smaller threshold to ensure complete coverage
                    if (dist < radius * 0.8) {
                        cell.searched = true;
                        this.unsearchedCells.delete(key);
                    }
                }
            }
        }
    }
    
    getUnsearchedTarget(droneX, droneY) {
        if (this.unsearchedCells.size === 0) return null;
        
        const droneGridX = Math.floor(droneX / config.gridSize);
        const droneGridY = Math.floor(droneY / config.gridSize);
        
        // Search in expanding rings around the drone
        for (let radius = 0; radius < 30; radius++) {
            const candidates = [];
            
            for (let dx = -radius; dx <= radius; dx++) {
                for (let dy = -radius; dy <= radius; dy++) {
                    if (Math.abs(dx) === radius || Math.abs(dy) === radius) {
                        const key = `${droneGridX + dx},${droneGridY + dy}`;
                        
                        if (this.unsearchedCells.has(key)) {
                            const cell = this.grid.get(key);
                            candidates.push({
                                x: cell.centerX,
                                y: cell.centerY
                            });
                        }
                    }
                }
            }
            
            if (candidates.length > 0) {
                return candidates[Math.floor(Math.random() * candidates.length)];
            }
        }
        
        // Fallback: pick random unsearched cell
        if (this.unsearchedCells.size > 0) {
            const keys = Array.from(this.unsearchedCells);
            const randomKey = keys[Math.floor(Math.random() * keys.length)];
            const cell = this.grid.get(randomKey);
            return { x: cell.centerX, y: cell.centerY };
        }
        
        return null;
    }
    
    hasUnsearchedArea() {
        return this.unsearchedCells.size > 0;
    }
    
    getCoverage() {
        return this.totalCells > 0 ? (this.totalCells - this.unsearchedCells.size) / this.totalCells : 0;
    }
    
    draw(ctx) {
        // Draw only unsearched cells (very efficient)
        ctx.fillStyle = 'rgba(255, 100, 100, 0.4)';
        
        for (const key of this.unsearchedCells) {
            const cell = this.grid.get(key);
            ctx.fillRect(cell.x, cell.y, config.gridSize, config.gridSize);
        }
    }
}

// Drone class implementing boids algorithm
class Drone {
    constructor(x, y) {
        this.position = { x, y };
        this.velocity = {
            x: (Math.random() - 0.5) * 2,
            y: (Math.random() - 0.5) * 2
        };
        this.acceleration = { x: 0, y: 0 };
        this.isResting = false;
    }

    update(drones, searchAreas) {
        // Check if there are search areas
        const hasSearchAreas = searchAreas.some(area => area.hasUnsearchedArea());
        
        if (!hasSearchAreas) {
            this.isResting = true;
            this.velocity.x *= 0.95;
            this.velocity.y *= 0.95;
            return;
        }
        
        this.isResting = false;
        
        // Apply strategy-specific behaviors
        if (config.strategy === 'swarm') {
            // Apply swarm behaviors
            const separation = this.separate(drones);
            const alignment = this.align(drones);
            const cohesion = this.cohere(drones);
            const target = this.seekTarget(searchAreas);
            
            // Weight the forces
            separation.x *= config.separationWeight;
            separation.y *= config.separationWeight;
            alignment.x *= config.alignmentWeight;
            alignment.y *= config.alignmentWeight;
            cohesion.x *= config.cohesionWeight;
            cohesion.y *= config.cohesionWeight;
            target.x *= config.targetWeight;
            target.y *= config.targetWeight;
            
            // Apply forces
            this.applyForce(separation);
            this.applyForce(alignment);
            this.applyForce(cohesion);
            this.applyForce(target);
        } else if (config.strategy === 'nearest') {
            // Just seek nearest target, minimal swarm behavior
            const separation = this.separate(drones);
            const target = this.seekTarget(searchAreas);
            
            separation.x *= 0.5;
            separation.y *= 0.5;
            target.x *= 3.0;
            target.y *= 3.0;
            
            this.applyForce(separation);
            this.applyForce(target);
        } else if (config.strategy === 'grid') {
            // Grid sweep pattern
            this.gridSweepBehavior(drones, searchAreas);
        } else if (config.strategy === 'random') {
            // Random walk with target seeking
            const separation = this.separate(drones);
            const target = this.seekTarget(searchAreas);
            const randomForce = {
                x: (Math.random() - 0.5) * 0.5,
                y: (Math.random() - 0.5) * 0.5
            };
            
            separation.x *= 0.5;
            separation.y *= 0.5;
            target.x *= 1.5;
            target.y *= 1.5;
            
            this.applyForce(separation);
            this.applyForce(target);
            this.applyForce(randomForce);
        }
        
        // Update velocity and position
        this.velocity.x += this.acceleration.x;
        this.velocity.y += this.acceleration.y;
        
        // Limit speed
        const speed = Math.sqrt(this.velocity.x ** 2 + this.velocity.y ** 2);
        if (speed > config.maxSpeed) {
            this.velocity.x = (this.velocity.x / speed) * config.maxSpeed;
            this.velocity.y = (this.velocity.y / speed) * config.maxSpeed;
        }
        
        this.position.x += this.velocity.x;
        this.position.y += this.velocity.y;
        
        // Reset acceleration
        this.acceleration = { x: 0, y: 0 };
        
        // Wrap around edges
        this.wrapEdges();
        
        // Mark area as searched
        this.markSearched(searchAreas);
    }
    
    applyForce(force) {
        this.acceleration.x += force.x;
        this.acceleration.y += force.y;
    }
    
    separate(drones) {
        const steer = { x: 0, y: 0 };
        let count = 0;
        
        for (const other of drones) {
            const d = this.distance(other.position);
            if (other !== this && d > 0 && d < config.separationDistance) {
                const diff = {
                    x: this.position.x - other.position.x,
                    y: this.position.y - other.position.y
                };
                // Weight by distance
                diff.x /= d;
                diff.y /= d;
                steer.x += diff.x;
                steer.y += diff.y;
                count++;
            }
        }
        
        if (count > 0) {
            steer.x /= count;
            steer.y /= count;
        }
        
        return this.limitForce(steer);
    }
    
    align(drones) {
        const steer = { x: 0, y: 0 };
        let count = 0;
        
        for (const other of drones) {
            const d = this.distance(other.position);
            if (other !== this && d > 0 && d < config.alignmentDistance) {
                steer.x += other.velocity.x;
                steer.y += other.velocity.y;
                count++;
            }
        }
        
        if (count > 0) {
            steer.x /= count;
            steer.y /= count;
            
            // Normalize and scale
            const mag = Math.sqrt(steer.x ** 2 + steer.y ** 2);
            if (mag > 0) {
                steer.x = (steer.x / mag) * config.maxSpeed;
                steer.y = (steer.y / mag) * config.maxSpeed;
            }
            
            steer.x -= this.velocity.x;
            steer.y -= this.velocity.y;
        }
        
        return this.limitForce(steer);
    }
    
    cohere(drones) {
        const steer = { x: 0, y: 0 };
        let count = 0;
        
        for (const other of drones) {
            const d = this.distance(other.position);
            if (other !== this && d > 0 && d < config.cohesionDistance) {
                steer.x += other.position.x;
                steer.y += other.position.y;
                count++;
            }
        }
        
        if (count > 0) {
            steer.x /= count;
            steer.y /= count;
            return this.seek(steer);
        }
        
        return steer;
    }
    
    gridSweepBehavior(drones, searchAreas) {
        // Initialize grid position if not set
        if (!this.gridX) {
            const droneIndex = drones.indexOf(this);
            const spacing = 50;
            this.gridX = (droneIndex % 10) * spacing;
            this.gridY = Math.floor(droneIndex / 10) * spacing;
            this.sweepDirection = 1;
        }
        
        const target = this.seekTarget(searchAreas);
        const separation = this.separate(drones);
        
        // Sweep in horizontal pattern
        const sweepTarget = {
            x: this.gridX,
            y: this.position.y
        };
        
        // Move horizontally across the area
        if (Math.abs(this.position.x - sweepTarget.x) < 20) {
            this.gridX += this.sweepDirection * 40;
            if (this.gridX > canvas.width || this.gridX < 0) {
                this.sweepDirection *= -1;
                this.gridY += 40;
            }
        }
        
        const sweepForce = this.seek(sweepTarget);
        
        separation.x *= 0.5;
        separation.y *= 0.5;
        target.x *= 2.0;
        target.y *= 2.0;
        sweepForce.x *= 1.0;
        sweepForce.y *= 1.0;
        
        this.applyForce(separation);
        this.applyForce(target);
        this.applyForce(sweepForce);
    }
    
    seekTarget(searchAreas) {
        // Find nearest unsearched cell using grid-accelerated search
        let nearest = null;
        let minDist = Infinity;
        
        for (const area of searchAreas) {
            if (!area.hasUnsearchedArea()) continue;
            
            const target = area.getUnsearchedTarget(this.position.x, this.position.y);
            if (target) {
                const d = this.distance(target);
                if (d < minDist) {
                    minDist = d;
                    nearest = target;
                }
            }
        }
        
        if (nearest) {
            return this.seek(nearest);
        }
        
        return { x: 0, y: 0 };
    }
    
    seek(target) {
        const desired = {
            x: target.x - this.position.x,
            y: target.y - this.position.y
        };
        
        const mag = Math.sqrt(desired.x ** 2 + desired.y ** 2);
        if (mag > 0) {
            desired.x = (desired.x / mag) * config.maxSpeed;
            desired.y = (desired.y / mag) * config.maxSpeed;
        }
        
        const steer = {
            x: desired.x - this.velocity.x,
            y: desired.y - this.velocity.y
        };
        
        return this.limitForce(steer);
    }
    
    limitForce(force) {
        const mag = Math.sqrt(force.x ** 2 + force.y ** 2);
        if (mag > config.maxForce) {
            force.x = (force.x / mag) * config.maxForce;
            force.y = (force.y / mag) * config.maxForce;
        }
        return force;
    }
    
    distance(pos) {
        const dx = this.position.x - pos.x;
        const dy = this.position.y - pos.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    wrapEdges() {
        if (this.position.x < 0) this.position.x = canvas.width;
        if (this.position.x > canvas.width) this.position.x = 0;
        if (this.position.y < 0) this.position.y = canvas.height;
        if (this.position.y > canvas.height) this.position.y = 0;
    }
    
    markSearched(searchAreas) {
        for (const area of searchAreas) {
            area.markSearched(this.position.x, this.position.y, config.searchRadius);
        }
    }
    
    draw() {
        ctx.save();
        ctx.translate(this.position.x, this.position.y);
        
        // Rotate to face direction of movement
        const angle = Math.atan2(this.velocity.y, this.velocity.x);
        ctx.rotate(angle);
        
        // Draw drone
        ctx.fillStyle = this.isResting ? '#999' : '#667eea';
        ctx.beginPath();
        ctx.moveTo(config.droneSize * 2, 0);
        ctx.lineTo(-config.droneSize, config.droneSize);
        ctx.lineTo(-config.droneSize, -config.droneSize);
        ctx.closePath();
        ctx.fill();
        
        // Draw search radius (faint circle)
        ctx.strokeStyle = this.isResting ? 'rgba(150, 150, 150, 0.1)' : 'rgba(102, 126, 234, 0.2)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(0, 0, config.searchRadius, 0, Math.PI * 2);
        ctx.stroke();
        
        ctx.restore();
    }
}

// Initialize drones
function initDrones() {
    drones = [];
    for (let i = 0; i < config.droneCount; i++) {
        drones.push(new Drone(
            Math.random() * canvas.width,
            Math.random() * canvas.height
        ));
    }
}

// Drawing functionality
canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    currentPath = [];
    const rect = canvas.getBoundingClientRect();
    currentPath.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    });
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing) return;
    
    const rect = canvas.getBoundingClientRect();
    currentPath.push({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    });
});

canvas.addEventListener('mouseup', () => {
    if (isDrawing && currentPath.length > 2) {
        // Create new search area
        const area = new SearchArea([...currentPath]);
        searchAreas.push(area);
    }
    
    isDrawing = false;
    currentPath = [];
});

canvas.addEventListener('mouseleave', () => {
    if (isDrawing) {
        isDrawing = false;
        currentPath = [];
    }
});

// Point in polygon test (ray casting algorithm)
function isPointInPolygon(x, y, polygon) {
    let inside = false;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i].x, yi = polygon[i].y;
        const xj = polygon[j].x, yj = polygon[j].y;
        
        const intersect = ((yi > y) !== (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
}

// Draw search areas
function drawSearchAreas() {
    for (const area of searchAreas) {
        area.draw(ctx);
    }
}

// Calculate coverage
function updateCoverage() {
    if (searchAreas.length === 0) {
        document.getElementById('coverage').textContent = '0%';
        return;
    }
    
    let totalCoverage = 0;
    for (const area of searchAreas) {
        totalCoverage += area.getCoverage();
    }
    
    const percentage = ((totalCoverage / searchAreas.length) * 100).toFixed(1);
    document.getElementById('coverage').textContent = `${percentage}%`;
}

// Update statistics display
function updateStats() {
    document.getElementById('timeSteps').textContent = stats.timeSteps;
    
    if (stats.clearTimes.length > 0) {
        const lastClear = stats.clearTimes[stats.clearTimes.length - 1];
        document.getElementById('lastClearTime').textContent = lastClear;
        
        const avgClear = Math.round(stats.clearTimes.reduce((a, b) => a + b, 0) / stats.clearTimes.length);
        document.getElementById('avgClearTime').textContent = avgClear;
    }
}

// Animation loop
function animate() {
    // Clear canvas
    ctx.fillStyle = '#fafafa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Increment time steps
    stats.timeSteps++;
    
    // Draw search areas
    drawSearchAreas();
    
    // Draw current drawing
    if (isDrawing && currentPath.length > 0) {
        ctx.strokeStyle = '#ff6464';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(currentPath[0].x, currentPath[0].y);
        for (let i = 1; i < currentPath.length; i++) {
            ctx.lineTo(currentPath[i].x, currentPath[i].y);
        }
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    // Update and draw drones
    for (const drone of drones) {
        drone.update(drones, searchAreas);
        drone.draw();
    }
    
    // Check for newly cleared areas
    for (const area of searchAreas) {
        if (!area.hasUnsearchedArea() && !area.wasComplete) {
            area.wasComplete = true;
            area.clearedAt = stats.timeSteps;
            const clearTime = area.clearedAt - area.createdAt;
            stats.clearTimes.push(clearTime);
        }
    }
    
    // Update coverage and stats
    updateCoverage();
    updateStats();
    
    requestAnimationFrame(animate);
}

// Controls
document.getElementById('droneCount').addEventListener('input', (e) => {
    config.droneCount = parseInt(e.target.value);
    document.getElementById('droneCountValue').textContent = config.droneCount;
    
    // Add or remove drones
    while (drones.length < config.droneCount) {
        drones.push(new Drone(
            Math.random() * canvas.width,
            Math.random() * canvas.height
        ));
    }
    while (drones.length > config.droneCount) {
        drones.pop();
    }
});

document.getElementById('clearAreas').addEventListener('click', () => {
    searchAreas = [];
    stats.clearTimes = [];
    document.getElementById('lastClearTime').textContent = '-';
    document.getElementById('avgClearTime').textContent = '-';
});

document.getElementById('resetDrones').addEventListener('click', () => {
    initDrones();
});

// Strategy button handlers
document.querySelectorAll('.strategy-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Update active state
        document.querySelectorAll('.strategy-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Set strategy
        config.strategy = btn.dataset.strategy;
        
        // Reset drones for some strategies
        if (config.strategy === 'grid') {
            drones.forEach(drone => {
                drone.gridX = undefined;
                drone.gridY = undefined;
            });
        }
    });
});

// Initialize and start
initDrones();
animate();
