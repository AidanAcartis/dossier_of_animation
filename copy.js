window.addEventListener('load', function(){
    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const g = 9.81;
    const airDensity = 1.225;

    // Constantes de la phase de propulsion
    const thrust = 15;  // Force de propulsion augmentée (N)
    const particleMass = 0.01;  // Masse des particules (kg)
    const gravity = 0.0981;
    const maxAltitude = 300;

    // Constantes de la phase d'explosion
    const explosionForce = 50;  // Force d'explosion (N)
    const deltaT = 1 / 60;  // Intervalle de temps (1/60s pour 60 FPS)
    const C = 10;  // Constante pour ajuster la vitesse initiale en fonction de l'explosion
    const radiusExplosion = 400;  // Rayon approximatif de l'explosion

    // Paramètres pour la vitesse initiale des particules
    const k = explosionForce / C;  // Facteur d'intensité de la vitesse initiale
    const r = radiusExplosion / 2;  // Distance moyenne des particules par rapport au centre de l'explosion
    const maxExplosionRadius = radiusExplosion * 0.8;  // Limiter l'explosion à 80% du rayon total

    class Particle {
        constructor(effect, x, y, color) {
            this.phase = "propulsion";  // Phase initiale (propulsion)
            this.effect = effect;
            this.startX = this.effect.centerX; // Centre en bas de l'écran
            this.startY = this.effect.height;
    
            // Légère dispersion autour du bas-centre
            this.x = this.startX + (Math.random() - 0.5) * 5; // Réduire la distance horizontale
            this.y = this.startY + (Math.random() - 0.5) * 5; // Réduire la distance verticale

            this.originX = Math.floor(x);
            this.originY = Math.floor(y);
            this.color = color;
            this.size = this.effect.gap;

            this.vx = (Math.random() - 0.5) * 0.8; // Réduire la vitesse horizontale
            this.vy = -Math.random() * 15 - 10; // Augmenter la vitesse de propulsion

            this.ease = 0.2;
            this.ax = 0;
            this.ay = 0;
    
            this.mass = particleMass;
            this.Fnet = 0;
            this.isReturning = false; // Indique si la particule est en phase de retour
            this.explosionSpeed = 30;
            this.explosionTime = null;
        }

        // Applique les forces en fonction de la phase
        applyForces() {
            switch(this.phase) {
                case 'propulsion':
                    // Augmenter la vitesse de propulsion
                    this.vx = (Math.random() - 0.5) * 0.8; // Réduire la distance horizontale
                    this.vy = -Math.random() * 15 - 10; // Augmenter la vitesse de propulsion

                    this.airResistanceForce = 0.5 * airDensity * Math.pow(this.vy, 2) * this.size;  // Force de résistance de l'air
                    this.Fnet = thrust - (gravity) - this.airResistanceForce; // Force nette en vertical
                    this.ax = 0;  // Pas de mouvement horizontal (donc ax = 0)
                    this.ay = this.Fnet / this.mass;  // Accélération verticale (propulsion + gravité + résistance de l'air)
                    break;
    
            
               case 'explosion':
                    // Calculer la distance par rapport au centre de l'explosion
                    const dx = this.x - this.effect.centerX;
                    const dy = this.y - this.effect.centerY;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    // Calculer la force de dispersion en fonction de la distance par rapport au centre
                    const explosionStrength = Math.max(0, explosionForce - (distance / radiusExplosion) * explosionForce);

                    // Calculer une direction aléatoire pour chaque particule dans la phase d'explosion
                    const angle = Math.random() * Math.PI * 2; // Angle aléatoire autour du centre
                    const speed = explosionStrength / this.mass;  // Vitesse de la particule en fonction de la force d'explosion

                    // Appliquer une accélération radiale (vers l'extérieur)
                    this.ax = Math.cos(angle) * speed;
                    this.ay = Math.sin(angle) * speed;

                    // Augmenter légèrement la vitesse de la particule pour simuler la dispersion
                    this.vx += this.ax * deltaT;
                    this.vy += this.ay * deltaT;

                    // Appliquer la force de résistance de l'air durant la phase d'explosion
                    this.airResistanceForce = 0.5 * airDensity * Math.pow(this.vy, 2) * this.size;
                    this.Fnet = -gravity - this.airResistanceForce; // Force nette verticale

                    // Limiter la position de la particule pour qu'elle ne dépasse pas la zone d'explosion
                    const maxDistance = Math.min(distance, maxExplosionRadius); // Limiter la distance à la limite maximale
                    this.x = this.effect.centerX + Math.cos(angle) * maxDistance;
                    this.y = this.effect.centerY + Math.sin(angle) * maxDistance;
                    // Vérifier si la dispersion est suffisante (en mesurant le diamètre du cercle)
                    const maxDist = Math.max(Math.abs(this.x - this.startX), Math.abs(this.y - this.startY));
                    if (maxDist > radiusExplosion) {
                        this.phase = "return";  // Passer à la phase de retour
                    }
                    break;



                case 'return':
                    this.vx = 0;
                    this.vy = 0;
                    this.ax = 0;
                    this.ay = 0;
                    break;
    
                default:
                    break;
            }
        }
    
    
        draw(context) {
            context.fillStyle = this.color;
            context.fillRect(this.x, this.y, this.size, this.size);
        }
    
        update() {
            if (this.phase === "propulsion") {
                // Montée avec décélération
                this.applyForces(); // Appliquer les forces d'explosion
                this.move(); // Déplacer la particule selon l'explosion

                if (this.y <= maxAltitude) { // Arrivé à 30% de la hauteur totale
                    this.phase = "explosion";  // Passer à la phase explosion
                }
            }
    
            else if (this.phase === "explosion") {
                // Phase d'explosion, dispersion des particules
                this.applyForces(); // Appliquer les forces d'explosion
                this.move(); // Déplacer la particule selon l'explosion
            }
                
            // Si la particule a fini l'explosion, elle retourne vers sa position d'origine
            else if (this.phase === "return") {
                this.x += (this.originX - this.x) * this.ease;
                this.y += (this.originY - this.y) * this.ease;
            }
        }

        move() {
            // Calculer la nouvelle vitesse en fonction de l'accélération
            this.vx += this.ax * deltaT;  // Vitesse horizontale, intégration de l'accélération
            this.vy += this.ay * deltaT;  // Vitesse verticale, intégration de l'accélération
    
            // Calculer la nouvelle position en fonction de la vitesse
            this.x += this.vx * deltaT;  // Position horizontale, intégration de la vitesse
            this.y += this.vy * deltaT;  // Position verticale, intégration de la vitesse
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
            this.gap = 2;
        }

        init(context){
            context.drawImage(this.image, this.X, this.Y);
            const pixels = context.getImageData(0, 0, this.width, this.height).data;

            for (let y = 0; y < this.height; y += this.gap){
                for (let x = 0; x < this.width; x += this.gap){
                    const index = (y * this.width + x) * 4;
                    const red = pixels[index];
                    const green = pixels[index + 1];
                    const blue = pixels[index + 2];
                    const alpha = pixels[index + 3];
                    const color = 'rgb(' + red + ',' + green + ',' + blue + ')';

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
        window.requestAnimationFrame(animate);
    }
    
    animate();
});
