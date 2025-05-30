window.addEventListener('load', function(){
    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext('2d');
    //console.log(ctx);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;


    class Particle {
        constructor(effect, x, y, color){
            this.effect = effect;
            this.x = Math.random() * this.effect.width;
            this.y = Math.random() * this.effect.height;
            this.originX = Math.floor(x);
            this.originY = Math.floor(y);
            this.color = color;
            this.size = this.effect.gap;
            this.vx = 0;
            this.vy = 0;
        }
        draw(context) {
            context.fillStyle = this.color;
            context.fillRect(this.x, this.y, this.size, this.size);
        }
        update(){
            this.x += (this.originX - this.x) * this.ease;
            this.y += (this.originY - this.y) * this.ease;
        }
    }

    class Effect {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.particlesArray = [];
            this.image = document.getElementById("image1");
            console.log(this.image.width);
            this.centerX = this.width * 0.5;
            this.centerY = this.height * 0.5;
            this.X = this.centerX - this.image.width * 0.5;
            this.Y = this.centerY - this.image.height * 0.5;
            this.gap = 2;

        }
        init(context){
            context.drawImage(this.image, this.X, this.Y);
            const pixels = context.getImageData(0, 0, this.width, this.height).data;
            for (let y = 0; y < this.height; y += this.gap){
                for (let x = 0; x < this.width; x += this.gap)
                    {
                    const index = (y * this.width + x) * 4;
                    const red = pixels[index];
                    const green = pixels[index + 1]; // Correction
                    const blue = pixels[index + 2];
                    const alpha = pixels[index + 3];
                    const color = 'rgb(' + red + ',' + green + ',' + blue + ')';

                    if (alpha > 0){
                        this.particlesArray.push(new Particle(this, x, y, color));
                    }
                }

            }
            // console.log(pixels);
        }
        draw(context){
            this.particlesArray.forEach(particle => particle.draw(context));
        
        }update(){
            this.particlesArray.forEach(particle => particle.update());   
        }
    }

    const effect = new Effect(canvas.width, canvas.height);
    effect.init(ctx);
    // console.log(effect);

    const particle1 = new Particle(effect);
    particle1.draw(ctx);

    function animate(){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        effect.draw(ctx);
        effect.update();
        window.requestAnimationFrame(animate);
    }
    animate();
    // ctx.fillRect(0, 0, 100, 200);
    // ctx.drawImage(image1, 100, 200, 400, 300);
 
});