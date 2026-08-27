const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let width = 0;
let height = 0;

let cx = 0;
let cy = 0;

let time = 0;
let rotation = 0;
let igrisState = "idle";

const particles = [];
const rings = [];
const energyLines = [];

const PARTICLE_COUNT = 1400;
const RING_COUNT = 8;
const ENERGY_COUNT = 24;


// ======================================================
// RESIZE
// ======================================================

function resize() {

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    width = window.innerWidth;
    height = window.innerHeight;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    cx = width * 0.5;
    cy = height * 0.49;
}


// ======================================================
// CREATE PARTICLES
// ======================================================

function createParticles() {

    particles.length = 0;

    for (let i = 0; i < PARTICLE_COUNT; i++) {

        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(
            2 * Math.random() - 1
        );

        particles.push({
            theta: theta,
            phi: phi,

            radius:
                0.78 + Math.random() * 0.22,

            size:
                0.35 + Math.random() * 1.4,

            alpha:
                0.2 + Math.random() * 0.7,

            phase:
                Math.random() * Math.PI * 2,

            speed:
                0.6 + Math.random() * 1.2
        });
    }
}


// ======================================================
// CREATE RINGS
// ======================================================

function createRings() {

    rings.length = 0;

    for (let i = 0; i < RING_COUNT; i++) {

        rings.push({

            radius:
                0.62 + i * 0.055,

            tilt:
                -0.75 + Math.random() * 1.5,

            rotation:
                Math.random() * Math.PI * 2,

            speed:
                0.8 + Math.random() * 0.8,

            alpha:
                0.2 + Math.random() * 0.3,

            width:
                0.7 + Math.random() * 1
        });
    }
}


// ======================================================
// CREATE ENERGY LINES
// ======================================================

function createEnergyLines() {

    energyLines.length = 0;

    for (let i = 0; i < ENERGY_COUNT; i++) {

        energyLines.push({

            side:
                i % 2 === 0
                    ? "blue"
                    : "orange",

            offset:
                (Math.random() - 0.5) * 2,

            amplitude:
                8 + Math.random() * 14,

            frequency:
                1.5 + Math.random() * 2,

            speed:
                0.8 + Math.random() * 1.2,

            phase:
                Math.random() * Math.PI * 2,

            thickness:
                i % 7 === 0
                    ? 2
                    : 0.8
        });
    }
}


// ======================================================
// 3D ROTATION
// ======================================================

function rotateY(x, y, z, angle) {

    const cos = Math.cos(angle);
    const sin = Math.sin(angle);

    return {

        x:
            x * cos -
            z * sin,

        y:
            y,

        z:
            x * sin +
            z * cos
    };
}


// ======================================================
// PROJECT 3D
// ======================================================

function project3D(x, y, z, scale) {

    const perspective =
        scale /
        (scale + z * 0.8);

    return {

        x:
            cx + x * perspective,

        y:
            cy + y * perspective,

        z:
            z,

        perspective:
            perspective
    };
}


// ======================================================
// DRAW SPHERE
// ======================================================

function drawSphere() {

    const radius =
        Math.min(width, height) * 0.23;

    const projectionScale =
        radius * 3.0;

    const points = [];

    for (const p of particles) {

        const sinPhi =
            Math.sin(p.phi);

        let x =
            sinPhi *
            Math.cos(p.theta) *
            radius *
            p.radius;

        let y =
            Math.cos(p.phi) *
            radius *
            p.radius;

        let z =
            sinPhi *
            Math.sin(p.theta) *
            radius *
            p.radius;

        const rotated =
            rotateY(
                x,
                y,
                z,
                rotation
            );

        x = rotated.x;
        y = rotated.y;
        z = rotated.z;

        const breathe =
            1 +
            Math.sin(
                time * 1.3 +
                p.phase
            ) * 0.012;

        x *= breathe;
        y *= breathe;

        const point =
            project3D(
                x,
                y,
                z,
                projectionScale
            );

        points.push({

            x: point.x,
            y: point.y,
            z: point.z,

            size:
                p.size *
                point.perspective,

            alpha:
                p.alpha *
                (
                    0.35 +
                    0.65 *
                    point.perspective
                )
                
        });
    }

    // Depth sorting
    points.sort(
        (a, b) => a.z - b.z
    );

    for (const p of points) {

        if (p.alpha < 0.05) {
            continue;
        }

        ctx.beginPath();

        ctx.fillStyle =
            `rgba(
                255,
                180,
                60,
                ${p.alpha}
            )`;

        ctx.shadowBlur =
            p.size > 1
                ? 4
                : 1;

        ctx.shadowColor =
            "rgba(255,150,30,0.7)";

        ctx.arc(
            p.x,
            p.y,
            p.size,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.shadowBlur = 0;
}



// ======================================================
// DRAW ROTATING RINGS
// ======================================================

function drawRings() {

    const baseRadius =
        Math.min(width, height) * 0.23;

    for (const ring of rings) {

        const radius =
            baseRadius *
            ring.radius;

        const vertical =
            Math.abs(
                Math.sin(
                    ring.tilt
                )
            );

        const angle =
            ring.rotation +
            time *
            ring.speed;

        ctx.save();

        ctx.translate(
            cx,
            cy
        );

        ctx.rotate(angle);

        ctx.beginPath();

        ctx.ellipse(
            0,
            0,
            radius,
            radius * vertical,
            0,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            `rgba(
                255,
                175,
                55,
                ${ring.alpha}
            )`;

        ctx.lineWidth =
            ring.width;

        ctx.shadowBlur = 7;

        ctx.shadowColor =
            "rgba(255,150,30,0.55)";

        ctx.stroke();

        ctx.restore();
    }

    ctx.shadowBlur = 0;
}


// ======================================================
// RINGS THROUGH CORE
// ======================================================

function drawCrossRings() {

    const radius =
        Math.min(width, height) * 0.23;

    // One continuous rotation for the whole structure
    const ringRotation = rotation;

    // ============================================
    // BACK HALF
    // ============================================

    ctx.save();

    ctx.translate(cx, cy);
    ctx.rotate(ringRotation);

    ctx.beginPath();

    ctx.ellipse(
        0,
        0,
        radius * 1.55,
        radius * 0.30,
        0,
        Math.PI,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "rgba(255, 175, 55, 0.22)";

    ctx.lineWidth = 1.2;

    ctx.shadowBlur = 4;
    ctx.shadowColor =
        "rgba(255, 140, 25, 0.35)";

    ctx.stroke();

    ctx.restore();


    // ============================================
    // FRONT HALF
    // ============================================

    ctx.save();

    ctx.translate(cx, cy);
    ctx.rotate(ringRotation);

    ctx.beginPath();

    ctx.ellipse(
        0,
        0,
        radius * 1.55,
        radius * 0.30,
        0,
        0,
        Math.PI
    );

    ctx.strokeStyle =
        "rgba(255, 205, 95, 0.72)";

    ctx.lineWidth = 1.8;

    ctx.shadowBlur = 10;
    ctx.shadowColor =
        "rgba(255, 155, 30, 0.7)";

    ctx.stroke();

    ctx.restore();


    // ============================================
    // VERTICAL RING
    // ============================================

    ctx.save();

    ctx.translate(cx, cy);
    ctx.rotate(-ringRotation * 0.7);

    ctx.beginPath();

    ctx.ellipse(
        0,
        0,
        radius * 0.36,
        radius * 1.40,
        0,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "rgba(255, 195, 70, 0.28)";

    ctx.lineWidth = 1.1;

    ctx.shadowBlur = 5;

    ctx.stroke();

    ctx.restore();

    ctx.shadowBlur = 0;
}

// ======================================================
// ENERGY STREAMS
// ======================================================

function drawEnergyStreams() {

    const centerY = cy;

    const outerX = width * 0.49;
    const coreX = Math.min(width, height) * 0.235;

    const strands = 18;

    // =====================================================
    // LEFT BLUE ENERGY
    // =====================================================

    for (let i = 0; i < strands; i++) {

        const spread =
            (i - (strands - 1) / 2) * 9;

        const startX = cx - outerX;
        const endX = cx - coreX;

        const points = [];

        for (let p = 0; p <= 20; p++) {

            const t = p / 20;

            const x =
                startX +
                (endX - startX) * t;

            // Energy is wider outside and tighter near core
            const envelope =
                1 - t * 0.78;

            const wobble =
                Math.sin(
                    time * 1.8 +
                    i * 1.37 +
                    t * 11
                ) * 10 * envelope;

            const jitter =
                Math.sin(
                    time * 2.7 +
                    i * 2.1 +
                    t * 29
                ) * 3.5 * envelope;

            const y =
                centerY +
                spread * envelope +
                wobble +
                jitter;

            points.push({ x, y });
        }

        ctx.beginPath();

        ctx.moveTo(
            points[0].x,
            points[0].y
        );

        for (let p = 1; p < points.length; p++) {

            ctx.lineTo(
                points[p].x,
                points[p].y
            );
        }

        const strong =
            i === 3 ||
            i === 8 ||
            i === 14;

        ctx.strokeStyle =
            strong
                ? "rgba(70,200,255,0.58)"
                : "rgba(30,160,255,0.24)";

        ctx.lineWidth =
            strong
                ? 1.8
                : 0.8;

        ctx.shadowBlur =
            strong
                ? 9
                : 3;

        ctx.shadowColor =
            "rgba(30,170,255,0.7)";

        ctx.stroke();
    }


    // =====================================================
    // LEFT BRIGHT ENERGY TENDRILS
    // =====================================================

    for (let i = 0; i < 5; i++) {

        const path = new Path2D();

        const startX =
            cx - outerX;

        const endX =
            cx - coreX * 0.72;

        const y =
            centerY +
            (i - 2) * 12;

        path.moveTo(
            startX,
            y
        );

        const c1x =
            startX +
            (endX - startX) * 0.30;

        const c1y =
            y +
            Math.sin(time * 2 + i) * 22;

        const c2x =
            startX +
            (endX - startX) * 0.65;

        const c2y =
            centerY +
            (i - 2) * 5 +
            Math.sin(time * 3 + i) * 10;

        path.bezierCurveTo(
            c1x,
            c1y,
            c2x,
            c2y,
            endX,
            centerY
        );

        ctx.strokeStyle =
            "rgba(100,220,255,0.55)";

        ctx.lineWidth = 1.4;

        ctx.shadowBlur = 10;

        ctx.shadowColor =
            "rgba(50,190,255,0.8)";

        ctx.stroke(path);
    }


    // =====================================================
    // RIGHT ORANGE ENERGY
    // =====================================================

    for (let i = 0; i < strands; i++) {

        const spread =
            (i - (strands - 1) / 2) * 9;

        const startX = cx + outerX;
        const endX = cx + coreX;

        const points = [];

        for (let p = 0; p <= 20; p++) {

            const t = p / 20;

            const x =
                startX -
                (startX - endX) * t;

            const envelope =
                1 - t * 0.78;

            const wobble =
                Math.sin(
                    time * 1.8 +
                    i * 1.51 +
                    t * 12
                ) * 10 * envelope;

            const jitter =
                Math.sin(
                    time * 2.5 +
                    i * 1.9 +
                    t * 31
                ) * 3.5 * envelope;

            const y =
                centerY +
                spread * envelope +
                wobble +
                jitter;

            points.push({ x, y });
        }

        ctx.beginPath();

        ctx.moveTo(
            points[0].x,
            points[0].y
        );

        for (let p = 1; p < points.length; p++) {

            ctx.lineTo(
                points[p].x,
                points[p].y
            );
        }

        const strong =
            i === 2 ||
            i === 9 ||
            i === 15;

        ctx.strokeStyle =
            strong
                ? "rgba(255,125,40,0.58)"
                : "rgba(255,90,25,0.24)";

        ctx.lineWidth =
            strong
                ? 1.8
                : 0.8;

        ctx.shadowBlur =
            strong
                ? 9
                : 3;

        ctx.shadowColor =
            "rgba(255,95,25,0.75)";

        ctx.stroke();
    }


    // =====================================================
    // RIGHT BRIGHT ENERGY TENDRILS
    // =====================================================

    for (let i = 0; i < 5; i++) {

        const path = new Path2D();

        const startX =
            cx + outerX;

        const endX =
            cx + coreX * 0.72;

        const y =
            centerY +
            (i - 2) * 12;

        path.moveTo(
            startX,
            y
        );

        const c1x =
            startX -
            (startX - endX) * 0.30;

        const c1y =
            y +
            Math.sin(time * 2 + i + 1) * 22;

        const c2x =
            startX -
            (startX - endX) * 0.65;

        const c2y =
            centerY +
            (i - 2) * 5 +
            Math.sin(time * 3 + i + 2) * 10;

        path.bezierCurveTo(
            c1x,
            c1y,
            c2x,
            c2y,
            endX,
            centerY
        );

        ctx.strokeStyle =
            "rgba(255,145,55,0.55)";

        ctx.lineWidth = 1.4;

        ctx.shadowBlur = 10;

        ctx.shadowColor =
            "rgba(255,105,30,0.8)";

        ctx.stroke(path);
    }

    ctx.shadowBlur = 0;
}


// ======================================================
// ENERGY PARTICLES
// ======================================================

function drawEnergyParticles() {

    const radius =
        Math.min(width, height) * 0.28;

    for (let i = 0; i < 80; i++) {

        const angle =
            i * 0.55 +
            time * 0.7;

        const distance =
            radius *
            (
                0.75 +
                Math.sin(
                    i * 1.7 +
                    time
                ) *
                0.12
            );

        const x =
            cx +
            Math.cos(angle) *
            distance;

        const y =
            cy +
            Math.sin(angle) *
            distance;

        ctx.beginPath();

        ctx.fillStyle =
            i % 2 === 0
                ? "rgba(255,185,65,0.65)"
                : "rgba(60,190,255,0.35)";

        ctx.arc(
            x,
            y,
            0.7 +
            Math.random() * 1.3,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}


// ======================================================
// CORE GLOW
// ======================================================

function drawCoreGlow() {

    const radius =
        Math.min(width, height) * 0.26;

    const gradient =
        ctx.createRadialGradient(
            cx,
            cy,
            10,
            cx,
            cy,
            radius
        );

    gradient.addColorStop(
        0,
        "rgba(255,170,50,0.12)"
    );

    gradient.addColorStop(
        0.5,
        "rgba(255,100,30,0.04)"
    );

    gradient.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        cx - radius,
        cy - radius,
        radius * 2,
        radius * 2
    );
}


// ======================================================
// HOLOGRAM SCANLINES
// ======================================================

function drawScanlines() {

    const radius =
        Math.min(width, height) * 0.29;

    ctx.save();

    ctx.beginPath();

    ctx.arc(
        cx,
        cy,
        radius,
        0,
        Math.PI * 2
    );

    ctx.clip();

    for (
        let y = cy - radius;
        y < cy + radius;
        y += 4
    ) {

        ctx.fillStyle =
            "rgba(255,220,120,0.02)";

        ctx.fillRect(
            cx - radius,
            y,
            radius * 2,
            1
        );
    }

    ctx.restore();
}


// ======================================================
// ANIMATION LOOP
// ======================================================
function drawCoreActivity() {

    const baseRadius =
        Math.min(width, height) * 0.23;

    let glowStrength = 0.25;
    let coreSize = 6;
    let pulseSpeed = 1.2;

    if (igrisState === "listening") {
        glowStrength = 0.75;
        coreSize = 8;
        pulseSpeed = 2.5;
    }

    if (igrisState === "speaking") {
        glowStrength = 1.0;
        coreSize = 10;
        pulseSpeed = 5.0;
    }

    const pulse =
        0.85 +
        Math.sin(time * pulseSpeed) * 0.15;

    const radius =
        coreSize * pulse;

    const glow =
        ctx.createRadialGradient(
            cx,
            cy,
            0,
            cx,
            cy,
            baseRadius * 0.55
        );

    glow.addColorStop(
        0,
        `rgba(255,245,180,${glowStrength})`
    );

    glow.addColorStop(
        0.12,
        `rgba(255,190,55,${glowStrength * 0.8})`
    );

    glow.addColorStop(
        0.35,
        `rgba(255,120,20,${glowStrength * 0.28})`
    );

    glow.addColorStop(
        1,
        "rgba(255,100,20,0)"
    );

    ctx.fillStyle = glow;

    ctx.beginPath();

    ctx.arc(
        cx,
        cy,
        baseRadius * 0.55,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.fillStyle =
        `rgba(255,250,215,${0.75 + glowStrength * 0.25})`;

    ctx.shadowBlur =
        igrisState === "speaking"
            ? 25
            : igrisState === "listening"
                ? 18
                : 8;

    ctx.shadowColor =
        "rgba(255,170,40,0.95)";

    ctx.arc(
        cx,
        cy,
        radius,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.shadowBlur = 0;
}
function setIgrisState(state) {

    if (
        state === "idle" ||
        state === "listening" ||
        state === "speaking"
    ) {
        igrisState = state;
    }
} 


function render() {

    // These two values MUST change every frame.
    time += 0.018;
    rotation += 0.004;

    ctx.clearRect(
        0,
        0,
        width,
        height
    );

    drawCoreGlow();

    drawEnergyStreams();

    drawRings();

    drawSphere();

    drawCrossRings();

    drawCoreActivity();

    drawEnergyParticles();

    drawScanlines();

    requestAnimationFrame(render);
}


// ======================================================
// START
// ======================================================

window.addEventListener(
    "resize",
    resize
);

resize();

createParticles();
createRings();
createEnergyLines();

render();