Voici une version améliorée de votre code, ajoutant les forces de propulsion, gravité, résistance de l'air et explosion pour chaque phase, ainsi que les calculs d'accélération correspondants :

```javascript
window.addEventListener('load', function(){
    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const g = 9.81;  // Accélération due à la gravité (m/s²)
    const airDensity = 1.225;  // Densité de l'air (kg/m³)

    // Constantes de la phase de propulsion
    const thrust = 10;  // Force de propulsion (N)
    const particleMass = 0.01;  // Masse des particules (kg)

    // Constantes de la phase d'explosion
    const explosionForce = 50;  // Force d'explosion (N)

    class Particle {
        constructor(effect, x, y, color, phase) {
            this.effect = effect;
            this.x = x;
            this.y = y;
            this.color = color;
            this.size = this.effect.gap;
            this.vx = 0;
            this.vy = 0;
            this.ax = 0;
            this.ay = 0;
            this.phase = phase;  // Phase de la particule (propulsion, explosion, etc.)
            this.mass = particleMass;
        }

        draw(context) {
            context.fillStyle = this.color;
            context.fillRect(this.x, this.y, this.size, this.size);
        }

        update() {
            this.applyForces();
            this.move();
        }

        // Applique les forces en fonction de la phase
        applyForces() {
            switch(this.phase) {
                case 'propulsion':
                    this.ax = thrust / this.mass;  // Accélération due à la propulsion
                    this.ay = -g;  // Gravité (force vers le bas)
                    break;
                case 'gravity':
                    this.ax = 0;
                    this.ay = -g;  // Gravité seulement
                    break;
                case 'airResistance':
                    let airResistanceForce = 0.5 * airDensity * this.vx * this.vx * this.size;
                    this.ax = -airResistanceForce / this.mass;
                    this.ay = -g;  // Gravité et résistance de l'air
                    break;
                case 'explosion':
                    this.ax = explosionForce / this.mass;
                    this.ay = explosionForce / this.mass;  // Explosion en toutes directions
                    break;
                default:
                    this.ax = 0;
                    this.ay = -g;  // Par défaut, seulement la gravité
                    break;
            }
        }

        move() {
            this.vx += this.ax;
            this.vy += this.ay;
            this.x += this.vx;
            this.y += this.vy;
        }
    }

    class Effect {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.particlesArray = [];
            this.gap = 2;
            this.phase = 'propulsion';  // Phase initiale
        }

        init(context) {
            // Exemple pour ajouter des particules
            const numParticles = 100;
            for (let i = 0; i < numParticles; i++) {
                let x = this.width * 0.5 + Math.random() * 10;
                let y = this.height * 0.5 + Math.random() * 10;
                let color = 'rgb(' + Math.random()*255 + ',' + Math.random()*255 + ',' + Math.random()*255 + ')';
                this.particlesArray.push(new Particle(this, x, y, color, this.phase));
            }
        }

        draw(context) {
            this.particlesArray.forEach(particle => particle.draw(context));
        }

        update() {
            this.particlesArray.forEach(particle => particle.update());
        }

        setPhase(phase) {
            this.phase = phase;
            this.particlesArray.forEach(particle => particle.phase = phase);  // Changer la phase pour toutes les particules
        }
    }

    const effect = new Effect(canvas.width, canvas.height);
    effect.init(ctx);

    // Fonction pour gérer l'animation
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        effect.draw(ctx);
        effect.update();

        // Exemple de changement de phase après un certain temps
        if (effect.phase === 'propulsion') {
            setTimeout(() => {
                effect.setPhase('gravity');  // Changer de phase après un certain délai
            }, 2000);  // Changer après 2 secondes

            setTimeout(() => {
                effect.setPhase('airResistance');  // Changer de phase après un certain délai
            }, 4000);  // Changer après 4 secondes

            setTimeout(() => {
                effect.setPhase('explosion');  // Changer de phase après un certain délai
            }, 6000);  // Changer après 6 secondes
        }

        window.requestAnimationFrame(animate);
    }

    animate();
});
```

### Explications :
1. **Forces et Accélérations :** 
    - La **propulsion** applique une force de poussée constante qui donne une accélération. La gravité est également prise en compte, agissant vers le bas.
    - La **gravité** applique uniquement une accélération due à la gravité (vers le bas) sans d'autres forces.
    - La **résistance de l'air** est calculée en utilisant une formule simplifiée pour les particules qui se déplacent dans l'air. La résistance est calculée en fonction de la vitesse de la particule et de sa taille.
    - L'**explosion** applique une force radiale uniforme sur la particule dans toutes les directions.

2. **Phases :**
    - La classe `Effect` contient un champ `phase` pour définir quelle phase est active (par défaut, c'est la propulsion). 
    - La fonction `setPhase` permet de changer la phase pour toutes les particules en même temps.
  
3. **Changement de phase :**
    - Après un certain délai (2, 4 et 6 secondes), le code change la phase pour simuler une transition entre la propulsion, la gravité, la résistance de l'air, et l'explosion.

Cela permet de modéliser le mouvement des particules sous différentes forces, tout en gérant les transitions entre les différentes phases.