class FireworkPixelArtEffect {
    constructor(path = './Babe.png', pixelSize = 3, scale = 2) {
        this.pixelSize = pixelSize;
        this.scale = scale;
        this.imagePath = path;
        this.canvas = document.getElementById('fireworkCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.pixels = [];
        this.center = [0, 0];
        this.phase = 'propulsion';
        this.gravity = 0.05;
        this.explosionHeight = 300; // Set height of the explosion
        this.explosionTime = null;
        this.loadImage();
    }

    loadImage() {
        const img = new Image();
        img.onload = () => {
            this.image = img;
            this.WIDTH = img.width;
            this.HEIGHT = img.height;
            this.canvas.width = this.WIDTH * this.scale;
            this.canvas.height = this.HEIGHT * this.scale;
            this.center = [this.WIDTH / 2, this.HEIGHT - 50]; // Starting point of firework

            for (let x = 0; x < this.WIDTH; x += this.pixelSize) {
                for (let y = 0; y < this.HEIGHT; y += this.pixelSize) {
                    const block = this.ctx.getImageData(x, y, this.pixelSize, this.pixelSize);
                    const avgColor = this.getAverageColor(block.data);
                    this.pixels.push({
                        position: [...this.center],
                        finalPosition: [x, y],
                        color: avgColor,
                        velocity: [0, 0],
                        size: Math.random() * this.scale + 1,
                        exploded: false,
                        distanceToTravel: Math.sqrt(Math.pow(x - this.center[0], 2) + Math.pow(y - this.center[1], 2))
                    });
                }
            }
            this.run();
        };
        img.src = this.imagePath;
    }

    getAverageColor(data) {
        let r = 0, g = 0, b = 0;
        for (let i = 0; i < data.length; i += 4) {
            r += data[i];
            g += data[i + 1];
            b += data[i + 2];
        }
        const count = data.length / 4;
        return [Math.floor(r / count), Math.floor(g / count), Math.floor(b / count)];
    }

    updatePixels() {
        const currentTime = Date.now();

        if (this.phase === 'propulsion') {
            if (this.center[1] > this.explosionHeight) {
                this.center[1] -= 10;
                for (let pixel of this.pixels) {
                    if (pixel.velocity[0] === 0 && pixel.velocity[1] === 0) {
                        const angle = Math.random() * Math.PI * 2;
                        const speed = Math.random() * 5 + 4;
                        pixel.velocity = [speed * Math.cos(angle), speed * Math.sin(angle)];
                    }
                    pixel.position[0] = this.center[0] + pixel.velocity[0];
                    pixel.position[1] -= 10;
                }
            } else {
                this.phase = 'final';
            }
        } else if (this.phase === 'final') {
            if (this.explosionTime === null) {
                this.explosionTime = currentTime;
            }

            const explosionDuration = 3000;
            for (let pixel of this.pixels) {
                if (currentTime - this.explosionTime < explosionDuration) {
                    pixel.position[0] += Math.random() * 4 - 2;
                    pixel.position[1] += Math.random() * 4 - 2;
                }

                const [x, y] = pixel.position;
                const [fx, fy] = pixel.finalPosition;
                const distance = Math.sqrt(Math.pow(fx - x, 2) + Math.pow(fy - y, 2));
                const speed = distance / 30;

                if (distance > 1) {
                    pixel.position[0] += (fx - x) * speed / distance;
                    pixel.position[1] += (fy - y) * speed / distance;
                } else {
                    pixel.position = [fx, fy];
                }
            }
        }
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (this.phase === 'propulsion') {
            this.ctx.beginPath();
            this.ctx.arc(this.center[0] * this.scale, this.center[1] * this.scale, 5 * this.scale, 0, Math.PI * 2);
            this.ctx.fillStyle = 'white';
            this.ctx.fill();
        }

        if (this.phase !== 'final') {
            for (let pixel of this.pixels) {
                this.ctx.beginPath();
                this.ctx.arc(pixel.position[0] * this.scale, pixel.position[1] * this.scale, pixel.size, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgb(${pixel.color[0]}, ${pixel.color[1]}, ${pixel.color[2]})`;
                this.ctx.fill();
            }
        }

        if (this.phase === 'final') {
            for (let pixel of this.pixels) {
                this.ctx.beginPath();
                this.ctx.arc(pixel.position[0] * this.scale, pixel.position[1] * this.scale, pixel.size, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgb(${pixel.color[0]}, ${pixel.color[1]}, ${pixel.color[2]})`;
                this.ctx.fill();
            }
        }
    }

    saveImage() {
        const imageUrl = this.canvas.toDataURL();
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = 'final_firework_image.png';
        link.click();
    }

    run() {
        const loop = () => {
            this.updatePixels();
            this.draw();
            requestAnimationFrame(loop);
        };
        loop();
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 's') {
        fireworkEffect.saveImage();
    }
});

const fireworkEffect = new FireworkPixelArtEffect('./Babe.png', 1, 2);
