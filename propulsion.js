window.addEventListener('load', function(){
    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Particle {
        constructor(effect, x, y, color){
            this.effect = effect;
            this.startX = this.effect.centerX; 
            this.startY = this.effect.height;
            
            this.x = this.startX + (Math.random() - 0.5) * 10;
            this.y = this.startY + (Math.random() - 0.5) * 10;

            this.originX = Math.floor(x);
            this.originY = Math.floor(y);
            this.color = color;
            this.size = this.effect.gap;

            // Vitesse initiale
            this.vx = (Math.random() - 0.5) * 2; // Léger mouvement horizontal
            this.vy = -Math.random() * 8 - 5; // Propulsion vers le haut

            // Phase de l'animation
            this.phase = "launch"; // Peut être "launch", "explode", "return"
            this.gravity = 0.2; // Gravité appliquée après explosion
            this.explosionSpeed = 5;
        }

        draw(context) {
            context.fillStyle = this.color;
            context.fillRect(this.x, this.y, this.size, this.size);
        }

        update(){
            if (this.phase === "launch") {
                // Montée avec décélération
                this.y += this.vy;
                this.vy += 0.15; // Décélération progressive
                
                if (this.y <= this.effect.height * 0.3) { // Arrivé à 30% de la hauteur totale
                    this.phase = "explode";
                    this.vx = (Math.random() - 0.5) * this.explosionSpeed;
                    this.vy = (Math.random() - 0.5) * this.explosionSpeed;
                }
            }

            else if (this.phase === "explode") {
                // Dispersion
                this.x += this.vx;
                this.y += this.vy;
                this.vy += this.gravity; // Ajout de la gravité

                if (Math.abs(this.vx) < 0.1 && Math.abs(this.vy) < 0.1) { // Quand l'explosion ralentit
                    this.phase = "return";
                }
            }

            else if (this.phase === "return") {
                // Retour progressif
                this.x += (this.originX - this.x) * 0.05;
                this.y += (this.originY - this.y) * 0.05;
            }
        }
    }

    class Effect {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.particlesArray = [];
            this.image = document.getElementById("image1");

            this.centerX = this.width * 0.5;
            this.centerY = this.height * 0.5;
            this.X = this.centerX - this.image.width * 0.5;
            this.Y = this.centerY - this.image.height * 0.5;
            this.gap = 3;
        }

        init(context){
            context.drawImage(this.image, this.X, this.Y);
            const pixels = context.getImageData(0, 0, this.width, this.height).data;

            for (let y = 0; y < this.height; y += this.gap){
                for (let x = 0; x < this.width; x += this.gap){
                    const index = (y * this.width + x) * 4;
                    const alpha = pixels[index + 3];
                    const color = `rgb(${pixels[index]}, ${pixels[index + 1]}, ${pixels[index + 2]})`;

                    if (alpha > 0){
                        this.particlesArray.push(new Particle(this, x, y, color));
                    }
                }
            }
        }

        draw(context){
            this.particlesArray.forEach(particle => particle.draw(context));
        }

        update(){
            this.particlesArray.forEach(particle => particle.update());
        }
    }

    const effect = new Effect(canvas.width, canvas.height);
    effect.init(ctx);

    function animate(){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        effect.draw(ctx);
        effect.update();
        requestAnimationFrame(animate);
    }
    
    animate();
});
