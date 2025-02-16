La physique des mouvements des poudres ou des palettes dans les feux d'artifice peut être décrite par des principes fondamentaux de **mécanique** et de **dynamique des fluides**. Chaque particule de poudre ou palette se déplace sous l'influence de diverses forces, telles que la **force de propulsion initiale**, la **gravité**, les **forces de résistance de l'air**, et les **forces internes** de l'explosion. Voici les détails mathématiques associés aux différentes phases du mouvement des particules :

### 1. **Phase de Propulsion Initiale : Mouvement vertical du projectile**

Au moment du tir du feu d'artifice, le moteur est allumé et une charge pyrotechnique génère une force de propulsion qui propulse le projectile vers le haut. Ce mouvement peut être modélisé à l’aide des **équations de mouvement rectiligne uniformément accéléré**.

#### Forces en jeu :
- **Force de propulsion** \( F_p \) qui est constante sur une certaine durée, générée par l'explosion des gaz. Cette force pousse le feu d'artifice vers le haut.
- **Gravité** \( F_g = m \cdot g \), où \( m \) est la masse du projectile et \( g \) l'accélération due à la gravité (environ \( 9.81 \, \text{m/s}^2 \)).
- **Résistance de l'air** \( F_{\text{air}} = \frac{1}{2} C_d \rho A v^2 \), où \( C_d \) est le coefficient de traînée, \( \rho \) est la densité de l'air, \( A \) est la surface frontale de l'objet, et \( v \) est la vitesse du projectile.

#### Équations du mouvement :
La force nette sur le feu d'artifice au début est donc :

\[
F_{\text{net}} = F_p - F_g - F_{\text{air}}
\]

L'accélération \( a \) du projectile est donnée par la deuxième loi de Newton :

\[
a = \frac{F_{\text{net}}}{m} = \frac{F_p - m \cdot g - \frac{1}{2} C_d \rho A v^2}{m}
\]

La vitesse \( v(t) \) et la position \( y(t) \) du feu d'artifice en fonction du temps sont ensuite obtenues en intégrant l’accélération :

\[
v(t) = \int a \, dt
\]

\[
y(t) = \int v(t) \, dt
\]

### 2. **Phase de Vol Ascendant : Après la poussée initiale, mouvement sous l'influence de la gravité**

Une fois la poussée initiale épuisée, la gravité devient la principale force agissant sur la particule. La particule continue à monter jusqu'à atteindre un point où la vitesse devient nulle, puis elle commence à redescendre.

#### Forces en jeu :
- **Gravité** \( F_g = m \cdot g \).
- **Résistance de l'air** \( F_{\text{air}} = \frac{1}{2} C_d \rho A v^2 \), mais avec une direction opposée au mouvement, ralentissant la particule.

L’équation de mouvement devient donc :

\[
F_{\text{net}} = - m \cdot g - \frac{1}{2} C_d \rho A v^2
\]

et l'accélération est :

\[
a = \frac{- m \cdot g - \frac{1}{2} C_d \rho A v^2}{m}
\]

Une fois de plus, on intègre pour obtenir la vitesse et la position pendant cette phase :

\[
v(t) = \int a \, dt
\]

\[
y(t) = \int v(t) \, dt
\]

La particule finit par atteindre la hauteur maximale lorsque \( v = 0 \). La hauteur maximale \( h_{\text{max}} \) est donnée par la relation :

\[
v^2 = v_0^2 - 2 g h_{\text{max}}
\]

où \( v_0 \) est la vitesse initiale de la particule lors de la poussée et \( h_{\text{max}} \) est la hauteur maximale.

### 3. **Phase de Descente : Retour sous l'influence de la gravité**

Après la montée, la particule entame sa descente sous l'effet de la gravité. Pendant cette phase, la particule est soumise aux mêmes forces, mais la direction du mouvement est inversée. La résistance de l'air ralentit également le mouvement de la particule, mais à un taux plus lent au fur et à mesure qu'elle perd de la vitesse.

#### Forces en jeu :
- **Gravité** \( F_g = m \cdot g \).
- **Résistance de l'air** \( F_{\text{air}} = \frac{1}{2} C_d \rho A v^2 \), qui s'oppose au mouvement vers le bas.

L'équation du mouvement devient :

\[
F_{\text{net}} = m \cdot g - \frac{1}{2} C_d \rho A v^2
\]

L’accélération devient donc :

\[
a = \frac{m \cdot g - \frac{1}{2} C_d \rho A v^2}{m}
\]

En intégrant cette expression, on obtient la vitesse et la position de la particule pendant la descente :

\[
v(t) = \int a \, dt
\]

\[
y(t) = \int v(t) \, dt
\]

### 4. **Phase de Dispersal : Explosion et Éclatement**

Lorsqu'un feu d'artifice explose à une certaine hauteur, les particules se dispersent en fonction de la vitesse de l’explosion et de la force générée par les gaz qui s’échappent. Ces particules suivent une **trajectoire parabolique** sous l’influence de la gravité, mais leur mouvement est plus complexe en raison de la forte accélération initiale due à l'explosion.

#### Forces en jeu :
- **Force d'explosion** \( F_{\text{explosion}} \), qui génère une vitesse initiale \( v_{\text{explosion}} \) pour chaque particule.
- **Gravité** \( F_g = m \cdot g \).
- **Résistance de l'air** \( F_{\text{air}} = \frac{1}{2} C_d \rho A v^2 \), qui agit en opposition au mouvement.

La vitesse initiale de chaque particule après l'explosion dépend de sa position dans la charge pyrotechnique. Les particules qui sont plus proches du centre de l'explosion auront une vitesse initiale plus élevée, tandis que celles plus éloignées auront une vitesse initiale plus faible. Chaque particule suit une trajectoire parabolique donnée par l’équation du mouvement suivant la loi de Newton pour les forces agissant dessus :

\[
F_{\text{net}} = F_{\text{explosion}} - m \cdot g - \frac{1}{2} C_d \rho A v^2
\]

L'accélération est :

\[
a = \frac{F_{\text{net}}}{m} = \frac{F_{\text{explosion}} - m \cdot g - \frac{1}{2} C_d \rho A v^2}{m}
\]

Cette équation de mouvement décrit le déplacement des particules lors de l'explosion.

### Conclusion

Les mouvements des particules dans un feu d'artifice peuvent être modélisés par une combinaison de **mouvement rectiligne uniforme accéléré** lors de la propulsion, suivi de **mouvement parabolique sous gravité** lors de la montée et de la descente, et de **trajectoires explosives complexes** après l'explosion. Les forces principales en jeu sont la **poussée initiale**, la **gravité** et la **résistance de l'air**, et chaque phase du mouvement peut être décrite par des équations différentielles qui décrivent l'évolution de la vitesse et de la position des particules au cours du temps.