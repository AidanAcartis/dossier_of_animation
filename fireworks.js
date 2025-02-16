const canvas = document.getElementById('fireworkCanvas');
const ctx = canvas.getContext('2d');

let width, height;
let fireworkPixels = [];
let center = { x: 0, y: 0 };
let phase = "propulsion";
let startTime = Date.now();
let explosionHeight = 200;
let gravity = 0.05;
let explosionTime = null;
let scale = 2;

function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    center = { x: width / 2, y: height - 50 };
}

function FireworkPixel(x, y, color, size) {
    this.position = { x: center.x, y: center.y };
    this.finalPosition = { x: x, y: y };
    this.color = color;
    this.size = size;
    this.velocity = { x: 0, y: 0 };
    this.exploded = false;
    this.distanceToTravel = Math.sqrt(Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2));
}

function generatePixels(imageData) {
    fireworkPixels = [];
    for (let x = 0; x < imageData.width; x += 3) {
        for (let y = 0; y < imageData.height; y += 3) {
            const index = (y * imageData.width + x) * 4;
            const color = {
                r: imageData.data[index],
                g: imageData.data[index + 1],
                b: imageData.data[index + 2],
                a: imageData.data[index + 3]
            };
            fireworkPixels.push(new FireworkPixel(x, y, color, Math.random() * 2 + 1));
        }
    }
}

function updatePixels() {
    const currentTime = Date.now();
    
    if (phase === "propulsion") {
        if (center.y > explosionHeight) {
            center.y -= 10; // vitesse de propulsion
            fireworkPixels.forEach(pixel => {
                if (pixel.velocity.x === 0 && pixel.velocity.y === 0) {
                    const angle = Math.random() * 2 * Math.PI;
                    const speed = Math.random() * 5 + 4;
                    pixel.velocity.x = speed * Math.cos(angle);
                    pixel.velocity.y = speed * Math.sin(angle);
                }
                pixel.position.x += pixel.velocity.x;
                pixel.position.y -= 10; // propulsion verticale
            });
        } else {
            phase = "final";
            explosionTime = currentTime;
        }
    } else if (phase === "final") {
        const explosionDuration = 3000; // 3 secondes
        fireworkPixels.forEach(pixel => {
            if (currentTime - explosionTime < explosionDuration) {
                pixel.position.x += (Math.random() * 4 - 2); // variation horizontale
                pixel.position.y += (Math.random() * 4 - 2); // variation verticale
            }
            let dist = Math.sqrt(Math.pow(pixel.finalPosition.x - pixel.position.x, 2) + Math.pow(pixel.finalPosition.y - pixel.position.y, 2));
            if (dist > 1) {
                let speed = dist / 30;
                pixel.position.x += (pixel.finalPosition.x - pixel.position.x) * speed / dist;
                pixel.position.y += (pixel.finalPosition.y - pixel.position.y) * speed / dist;
            } else {
                pixel.position = { x: pixel.finalPosition.x, y: pixel.finalPosition.y };
            }
        });
    }
}

function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, width, height);

    if (phase === "propulsion") {
        ctx.beginPath();
        ctx.arc(center.x, center.y, 5 * scale, 0, Math.PI * 2);
        ctx.fillStyle = 'white';
        ctx.fill();
    }

    fireworkPixels.forEach(pixel => {
        ctx.beginPath();
        ctx.arc(pixel.position.x * scale, pixel.position.y * scale, pixel.size * scale, 0, Math.PI * 2);
        ctx.fillStyle = `rgb(${pixel.color.r}, ${pixel.color.g}, ${pixel.color.b})`;
        ctx.fill();
    });
}

function animate() {
    updatePixels();
    draw();
    requestAnimationFrame(animate);
}

resizeCanvas();
generatePixels({ width: 640, height: 480, data: new Uint8Array(640 * 480 * 4) }); // image vide ou à ajuster
animate();

window.addEventListener('resize', resizeCanvas);
