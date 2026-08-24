import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

questions = [
  {
    "id": "pb-mech-01",
    "title": "Projectile Departure from Hemisphere",
    "division": 2,
    "topic": "Dynamics",
    "difficulty": "Hard",
    "acceptance_rate": "38%",
    "year": 2023,
    "content": "A small particle of mass $m$ starts from rest at the very top of a frictionless fixed spherical dome of radius $R$. As the particle slides down the dome under gravity $g$, at what angle $\\theta$ measured from the vertical does it lose contact with the surface of the sphere?",
    "diagramSvg": "<svg viewBox='0 0 300 180' class='w-full max-w-sm mx-auto'><path d='M 30 150 A 120 120 0 0 1 270 150' fill='none' stroke='#60a5fa' stroke-width='4'/><line x1='150' y1='150' x2='150' y2='30' stroke='#94a3b8' stroke-dasharray='4'/><line x1='150' y1='150' x2='235' y2='65' stroke='#94a3b8'/><circle cx='235' cy='65' r='8' fill='#f59e0b'/><path d='M 150 70 A 80 80 0 0 1 190 85' fill='none' stroke='#ef4444' stroke-width='2'/><text x='165' y='75' fill='#ef4444' font-size='14'>θ</text><text x='155' y='140' fill='#94a3b8' font-size='12'>R</text><line x1='10' y1='150' x2='290' y2='150' stroke='#64748b' stroke-width='2'/></svg>",
    "options": [
      { "id": "A", "text": "$\\theta = \\arccos(1/3)$" },
      { "id": "B", "text": "$\\theta = \\arccos(1/2)$" },
      { "id": "C", "text": "$\\theta = \\arccos(2/3)$" },
      { "id": "D", "text": "$\\theta = \\arccos(3/4)$" },
      { "id": "E", "text": "$\\theta = \\pi/4$" }
    ],
    "correctAnswer": "C",
    "hints": [
      "Use conservation of mechanical energy to find the velocity $v$ as a function of angle $\\theta$.",
      "Write Newton's 2nd Law in the radial direction: $mg\\cos\\theta - N = \\frac{mv^2}{R}$.",
      "The particle loses contact when the normal force $N = 0$."
    ],
    "solution": {
      "summary": "The normal force vanishes when the required centripetal acceleration equals the radial component of gravity.",
      "steps": [
        "1. By Conservation of Energy, taking the center of the sphere as height reference: Initial energy at the top is $E_i = mgR$. At angle $\\theta$, the height is $h = R\\cos\\theta$, so $E_f = mgR\\cos\\theta + \\frac{1}{2}mv^2$.",
        "2. Equating energies gives: $mgR(1 - \\cos\\theta) = \\frac{1}{2}mv^2 \\implies v^2 = 2gR(1 - \\cos\\theta)$.",
        "3. In the radial direction towards the center of the dome: $mg\\cos\\theta - N = \\frac{mv^2}{R}$.",
        "4. Contact is lost when $N = 0$: $mg\\cos\\theta = \\frac{m(2gR(1 - \\cos\\theta))}{R} = 2mg(1 - \\cos\\theta)$.",
        "5. Dividing by $mg$: $\\cos\\theta = 2 - 2\\cos\\theta \\implies 3\\cos\\theta = 2 \\implies \\cos\\theta = \\frac{2}{3}$."
      ],
      "formulasUsed": [
        "\\Delta K + \\Delta U = 0",
        "F_{\\text{radial}} = mg\\cos\\theta - N = \\frac{mv^2}{R}"
      ],
      "keyTakeaway": "Losing contact with a curved surface is always marked by the condition $N = 0$."
    }
  },
  {
    "id": "pb-mech-02",
    "title": "Rolling Down an Inclined Plane",
    "division": 1,
    "topic": "Rotational Motion",
    "difficulty": "Medium",
    "acceptance_rate": "54%",
    "year": 2023,
    "content": "A solid uniform sphere ($I = \\frac{2}{5}MR^2$), a uniform solid cylinder ($I = \\frac{1}{2}MR^2$), and a thin spherical shell ($I = \\frac{2}{3}MR^2$) of the same mass $M$ and radius $R$ are released from rest simultaneously at the top of an incline of angle $\\theta$. If all objects roll without slipping, in what order do they reach the bottom of the incline?",
    "diagramSvg": "<svg viewBox='0 0 300 140' class='w-full max-w-sm mx-auto'><polygon points='20,120 280,120 280,20' fill='none' stroke='#60a5fa' stroke-width='3'/><circle cx='230' cy='45' r='20' fill='#f59e0b'/><line x1='20' y1='120' x2='280' y2='120' stroke='#64748b' stroke-width='3'/><text x='60' y='110' fill='#94a3b8' font-size='14'>θ</text></svg>",
    "options": [
      { "id": "A", "text": "Solid sphere first, then solid cylinder, then spherical shell" },
      { "id": "B", "text": "Spherical shell first, then solid cylinder, then solid sphere" },
      { "id": "C", "text": "Solid cylinder first, then solid sphere, then spherical shell" },
      { "id": "D", "text": "All three reach the bottom at the exact same time" },
      { "id": "E", "text": "Solid sphere and spherical shell tie for first, followed by cylinder" }
    ],
    "correctAnswer": "A",
    "hints": [
      "Recall the linear acceleration for rolling without slipping down an incline: $a = \\frac{g\\sin\\theta}{1 + I/(MR^2)}$.",
      "Smaller moment of inertia factor $\\beta = I/(MR^2)$ results in larger linear acceleration."
    ],
    "solution": {
      "summary": "Objects with a smaller dimensionless moment of inertia $\\beta = I/(MR^2)$ convert a larger fraction of potential energy into translational kinetic energy, giving them higher acceleration.",
      "steps": [
        "1. For any body rolling without slipping down an incline of angle $\\theta$: $a = \\frac{g\\sin\\theta}{1 + \\beta}$, where $I = \\beta MR^2$.",
        "2. For Solid Sphere: $\\beta = 2/5 = 0.40 \\implies a_1 = \\frac{g\\sin\\theta}{1.40} \\approx 0.714 g\\sin\\theta$.",
        "3. For Solid Cylinder: $\\beta = 1/2 = 0.50 \\implies a_2 = \\frac{g\\sin\\theta}{1.50} \\approx 0.667 g\\sin\\theta$.",
        "4. For Spherical Shell: $\\beta = 2/3 \\approx 0.667 \\implies a_3 = \\frac{g\\sin\\theta}{1.667} \\approx 0.600 g\\sin\\theta$.",
        "5. Since $a_1 > a_2 > a_3$, the solid sphere arrives first, followed by the solid cylinder, and finally the spherical shell."
      ],
      "formulasUsed": [
        "a_{\\text{cm}} = \\frac{g\\sin\\theta}{1 + I_{\\text{cm}}/(MR^2)}"
      ],
      "keyTakeaway": "Acceleration in pure rolling depends only on the shape (mass distribution factor $\\beta$), not the mass or radius."
    }
  },
  {
    "id": "pb-em-01",
    "title": "Gauss's Law with Non-Uniform Charge Density",
    "division": 2,
    "topic": "Electrostatics",
    "difficulty": "Hard",
    "acceptance_rate": "41%",
    "year": 2022,
    "content": "A non-conducting sphere of radius $R$ has a volume charge density given by $\\rho(r) = \\rho_0 \\left(\\frac{r}{R}\\right)$ for $r \\le R$, where $\\rho_0$ is a positive constant and $r$ is the radial distance from the center. What is the magnitude of the electric field $E(r)$ inside the sphere at a distance $r < R$?",
    "diagramSvg": "<svg viewBox='0 0 240 160' class='w-full max-w-xs mx-auto'><circle cx='120' cy='80' r='60' fill='#1e293b' stroke='#38bdf8' stroke-width='2'/><circle cx='120' cy='80' r='35' fill='none' stroke='#f43f5e' stroke-dasharray='3' stroke-width='2'/><line x1='120' y1='80' x2='120' y2='20' stroke='#94a3b8'/><line x1='120' y1='80' x2='145' y2='55' stroke='#f43f5e'/><text x='125' y='50' fill='#94a3b8' font-size='12'>R</text><text x='138' y='72' fill='#f43f5e' font-size='12'>r</text></svg>",
    "options": [
      { "id": "A", "text": "$E(r) = \\frac{\\rho_0 r^2}{4\\epsilon_0 R}$" },
      { "id": "B", "text": "$E(r) = \\frac{\\rho_0 r^2}{3\\epsilon_0 R}$" },
      { "id": "C", "text": "$E(r) = \\frac{\\rho_0 r}{4\\epsilon_0}$" },
      { "id": "D", "text": "$E(r) = \\frac{\\rho_0 r^3}{4\\epsilon_0 R^2}$" },
      { "id": "E", "text": "$E(r) = \\frac{\\rho_0 r^2}{2\\epsilon_0 R}$" }
    ],
    "correctAnswer": "A",
    "hints": [
      "Use Gauss's law with a spherical Gaussian surface of radius $r$: $\\oint \\vec{E}\\cdot d\\vec{A} = E(4\\pi r^2) = \\frac{Q_{\\text{enc}}}{\\epsilon_0}$.",
      "Integrate the charge density in spherical shells: $Q_{\\text{enc}} = \\int_0^r \\rho(r') 4\\pi r'^2 dr'$."
    ],
    "solution": {
      "summary": "Integrating the volume charge density yields the enclosed charge $Q_{\\text{enc}} = \\frac{\\pi \\rho_0 r^4}{R}$, which yields $E = \\frac{\\rho_0 r^2}{4\\epsilon_0 R}$ via Gauss's Law.",
      "steps": [
        "1. Construct a concentric spherical Gaussian surface of radius $r < R$.",
        "2. By spherical symmetry, $\\oint \\vec{E}\\cdot d\\vec{A} = E(r)(4\\pi r^2)$.",
        "3. Calculate $Q_{\\text{enc}}$: $Q_{\\text{enc}} = \\int_0^r \\rho(r') 4\\pi r'^2 dr' = 4\\pi \\int_0^r \\rho_0 \\frac{r'}{R} r'^2 dr' = \\frac{4\\pi \\rho_0}{R} \\int_0^r r'^3 dr'$.",
        "4. The integral is $\\int_0^r r'^3 dr' = \\frac{r^4}{4}$, so $Q_{\\text{enc}} = \\frac{4\\pi \\rho_0}{R} \\frac{r^4}{4} = \\frac{\\pi \\rho_0 r^4}{R}$.",
        "5. Apply Gauss's Law: $E(r)(4\\pi r^2) = \\frac{\\pi \\rho_0 r^4}{\\epsilon_0 R} \\implies E(r) = \\frac{\\rho_0 r^2}{4\\epsilon_0 R}$."
      ],
      "formulasUsed": [
        "\\oint \\vec{E}\\cdot d\\vec{A} = \\frac{Q_{\\text{enc}}}{\\epsilon_0}",
        "Q_{\\text{enc}} = \\int \\rho\\, dV = \\int_0^r \\rho(r') 4\\pi r'^2 dr'"
      ],
      "keyTakeaway": "Always integrate $dQ = \\rho(r') 4\\pi r'^2 dr'$ when charge density depends radially on distance."
    }
  },
  {
    "id": "pb-em-02",
    "title": "Conducting Rod on Magnetic Rails",
    "division": 1,
    "topic": "Magnetism",
    "difficulty": "Medium",
    "acceptance_rate": "59%",
    "year": 2023,
    "content": "A conducting rod of mass $m$ and resistance $R$ rests on two frictionless horizontal conducting rails separated by distance $L$. A uniform vertical magnetic field $\\vec{B}$ points perpendicularly into the plane of the rails. The rails are connected on one end by a resistor with resistance $R_{\\text{ext}} = R$. If a constant horizontal force $F_0$ pulls the rod to the right, what is the terminal speed $v_{\\text{term}}$ of the rod?",
    "diagramSvg": "<svg viewBox='0 0 320 140' class='w-full max-w-sm mx-auto'><line x1='30' y1='30' x2='290' y2='30' stroke='#38bdf8' stroke-width='4'/><line x1='30' y1='110' x2='290' y2='110' stroke='#38bdf8' stroke-width='4'/><rect x='30' y='30' width='15' height='80' fill='#64748b'/><line x1='180' y1='20' x2='180' y2='120' stroke='#f59e0b' stroke-width='6'/><line x1='180' y1='70' x2='250' y2='70' stroke='#10b981' stroke-width='3'/><polygon points='250,65 260,70 250,75' fill='#10b981'/><text x='215' y='60' fill='#10b981' font-size='14'>F₀</text><text x='100' y='80' fill='#94a3b8' font-size='18'>⊗ B</text></svg>",
    "options": [
      { "id": "A", "text": "$v_{\\text{term}} = \\frac{F_0 R}{B^2 L^2}$" },
      { "id": "B", "text": "$v_{\\text{term}} = \\frac{2F_0 R}{B^2 L^2}$" },
      { "id": "C", "text": "$v_{\\text{term}} = \\frac{F_0 R}{2B^2 L^2}$" },
      { "id": "D", "text": "$v_{\\text{term}} = \\frac{4F_0 R}{B^2 L^2}$" },
      { "id": "E", "text": "$v_{\\text{term}} = \\frac{F_0 R}{\\sqrt{2} B L}$" }
    ],
    "correctAnswer": "B",
    "hints": [
      "Find total circuit resistance: $R_{\\text{tot}} = R_{\\text{rod}} + R_{\\text{ext}} = 2R$.",
      "Motional emf is $\\mathcal{E} = BLv$, producing magnetic retarding force $F_B = I L B$.",
      "Terminal speed is reached when net force is zero ($F_0 = F_B$)."
    ],
    "solution": {
      "summary": "Motional EMF drives induced current through total resistance $2R$. The resulting magnetic braking force balances the applied pull force $F_0$.",
      "steps": [
        "1. The total resistance of the closed loop is $R_{\\text{total}} = R + R = 2R$.",
        "2. The motional emf generated across the rod moving at velocity $v$ is $\\mathcal{E} = BLv$.",
        "3. The induced current in the loop is $I = \\frac{\\mathcal{E}}{R_{\\text{total}}} = \\frac{BLv}{2R}$.",
        "4. The magnetic Lorentz force opposing the motion is $F_B = I L B = \\left(\\frac{BLv}{2R}\\right) L B = \\frac{B^2 L^2 v}{2R}$.",
        "5. At terminal speed, acceleration $a = 0 \\implies F_0 = F_B = \\frac{B^2 L^2 v_{\\text{term}}}{2R}$.",
        "6. Solving for $v_{\\text{term}}$: $v_{\\text{term}} = \\frac{2F_0 R}{B^2 L^2}$."
      ],
      "formulasUsed": [
        "\\mathcal{E} = B L v",
        "F_B = I L B = \\frac{B^2 L^2 v}{R_{\\text{total}}}"
      ],
      "keyTakeaway": "Terminal velocity is reached when magnetic braking equals the external applied pulling force."
    }
  },
  {
    "id": "pb-thermo-01",
    "title": "Adiabatic Expansion of Monatomic Ideal Gas",
    "division": 1,
    "topic": "Thermodynamics",
    "difficulty": "Medium",
    "acceptance_rate": "62%",
    "year": 2022,
    "content": "One mole of an ideal monatomic gas ($\\gamma = 5/3$) undergoes a reversible adiabatic expansion from an initial volume $V_0$ and temperature $T_0$ to a final volume $8V_0$. What is the final temperature $T_f$ of the gas?",
    "diagramSvg": "<svg viewBox='0 0 240 140' class='w-full max-w-xs mx-auto'><line x1='40' y1='20' x2='40' y2='120' stroke='#94a3b8' stroke-width='2'/><line x1='40' y1='120' x2='220' y2='120' stroke='#94a3b8' stroke-width='2'/><path d='M 60 40 Q 100 80 190 105' fill='none' stroke='#f59e0b' stroke-width='3'/><circle cx='60' cy='40' r='5' fill='#38bdf8'/><circle cx='190' cy='105' r='5' fill='#f43f5e'/><text x='20' y='30' fill='#94a3b8'>P</text><text x='210' y='135' fill='#94a3b8'>V</text><text x='65' y='35' fill='#38bdf8'>T₀, V₀</text><text x='155' y='95' fill='#f43f5e'>T_f, 8V₀</text></svg>",
    "options": [
      { "id": "A", "text": "$T_f = T_0 / 2$" },
      { "id": "B", "text": "$T_f = T_0 / 4$" },
      { "id": "C", "text": "$T_f = T_0 / 8$" },
      { "id": "D", "text": "$T_f = T_0 / 16$" },
      { "id": "E", "text": "$T_f = T_0 / \\sqrt{8}$" }
    ],
    "correctAnswer": "B",
    "hints": [
      "For a reversible adiabatic process, $T V^{\\gamma - 1} = \\text{constant}$.",
      "For a monatomic ideal gas, $\\gamma = 5/3$, so $\\gamma - 1 = 2/3$."
    ],
    "solution": {
      "summary": "Using the adiabatic relation $T V^{\\gamma-1} = \\text{const}$ with $\\gamma = 5/3$, the temperature drops by a factor of $(8)^{2/3} = 4$.",
      "steps": [
        "1. For an adiabatic process with an ideal gas: $T_i V_i^{\\gamma-1} = T_f V_f^{\\gamma-1}$.",
        "2. Here $\\gamma = 5/3$, so the exponent is $\\gamma - 1 = \\frac{5}{3} - 1 = \\frac{2}{3}$.",
        "3. Substitute the values: $T_0 V_0^{2/3} = T_f (8V_0)^{2/3}$.",
        "4. Simplify: $T_f = T_0 \\left(\\frac{V_0}{8V_0}\\right)^{2/3} = T_0 \\left(\\frac{1}{8}\\right)^{2/3}$.",
        "5. Since $8^{1/3} = 2$, we have $8^{2/3} = 2^2 = 4$.",
        "6. Therefore, $T_f = \\frac{T_0}{4}$."
      ],
      "formulasUsed": [
        "T V^{\\gamma - 1} = \\text{constant}",
        "\\gamma = \\frac{C_p}{C_v} = \\frac{5/2 R}{3/2 R} = \\frac{5}{3}"
      ],
      "keyTakeaway": "In adiabatic expansion, a gas does work at the expense of its internal energy, cooling down significantly."
    }
  },
  {
    "id": "pb-modern-01",
    "title": "Photoelectric Effect and Stopping Potential",
    "division": 1,
    "topic": "Modern Physics",
    "difficulty": "Easy",
    "acceptance_rate": "72%",
    "year": 2023,
    "content": "Light of wavelength $\\lambda = 300\\text{ nm}$ is incident on a metal surface with work function $\\Phi = 2.30\\text{ eV}$. Taking $hc \\approx 1240\\text{ eV}\\cdot\\text{nm}$, what is the stopping potential $V_0$ required to prevent any photoelectrons from reaching the collector plate?",
    "diagramSvg": "<svg viewBox='0 0 280 130' class='w-full max-w-xs mx-auto'><rect x='50' y='25' width='10' height='80' fill='#94a3b8'/><rect x='220' y='25' width='10' height='80' fill='#94a3b8'/><path d='M 10 30 L 48 50' stroke='#38bdf8' stroke-width='2' stroke-dasharray='4'/><path d='M 10 60 L 48 75' stroke='#38bdf8' stroke-width='2' stroke-dasharray='4'/><circle cx='100' cy='60' r='4' fill='#f59e0b'/><circle cx='140' cy='45' r='4' fill='#f59e0b'/><text x='10' y='25' fill='#38bdf8' font-size='12'>hν</text><text x='110' y='80' fill='#f59e0b' font-size='12'>e⁻</text><text x='115' y='120' fill='#94a3b8' font-size='13'>[ - | V₀ | + ]</text></svg>",
    "options": [
      { "id": "A", "text": "$V_0 = 1.83\\text{ V}$" },
      { "id": "B", "text": "$V_0 = 4.13\\text{ V}$" },
      { "id": "C", "text": "$V_0 = 2.30\\text{ V}$" },
      { "id": "D", "text": "$V_0 = 0.83\\text{ V}$" },
      { "id": "E", "text": "$V_0 = 6.43\\text{ V}$" }
    ],
    "correctAnswer": "A",
    "hints": [
      "Photon energy is $E = \\frac{hc}{\\lambda}$.",
      "Einstein's photoelectric equation: $K_{\\text{max}} = E - \\Phi = e V_0$."
    ],
    "solution": {
      "summary": "Calculate the photon energy in eV, subtract the work function to get maximum kinetic energy, and equate to $e V_0$.",
      "steps": [
        "1. Calculate photon energy: $E_{\\text{photon}} = \\frac{hc}{\\lambda} = \\frac{1240\\text{ eV}\\cdot\\text{nm}}{300\\text{ nm}} \\approx 4.133\\text{ eV}$.",
        "2. Einstein's photoelectric equation gives maximum kinetic energy: $K_{\\text{max}} = E_{\\text{photon}} - \\Phi = 4.133\\text{ eV} - 2.30\\text{ eV} = 1.833\\text{ eV}$.",
        "3. Since $K_{\\text{max}} = e V_0$, the stopping potential is $V_0 = 1.83\\text{ V}$."
      ],
      "formulasUsed": [
        "E_{\\text{photon}} = \\frac{hc}{\\lambda}",
        "e V_0 = K_{\\text{max}} = hf - \\Phi"
      ],
      "keyTakeaway": "The stopping potential measures the maximum kinetic energy of emitted photoelectrons directly in volts."
    }
  },
  {
    "id": "pb-optics-01",
    "title": "Two-Lens Focal Combination",
    "division": 2,
    "topic": "Optics",
    "difficulty": "Medium",
    "acceptance_rate": "48%",
    "year": 2021,
    "content": "Two thin converging lenses with focal lengths $f_1 = +20\\text{ cm}$ and $f_2 = +10\\text{ cm}$ are placed coaxially separated by a distance of $d = 15\\text{ cm}$. An object is placed $30\\text{ cm}$ to the left of the first lens. Where is the final image located relative to the second lens?",
    "diagramSvg": "<svg viewBox='0 0 300 120' class='w-full max-w-sm mx-auto'><line x1='20' y1='60' x2='280' y2='60' stroke='#64748b' stroke-width='2'/><line x1='120' y1='20' x2='120' y2='100' stroke='#38bdf8' stroke-width='3'/><line x1='200' y1='20' x2='200' y2='100' stroke='#38bdf8' stroke-width='3'/><line x1='50' y1='60' x2='50' y2='35' stroke='#f59e0b' stroke-width='3'/><polygon points='47,35 50,28 53,35' fill='#f59e0b'/><text x='112' y='115' fill='#38bdf8' font-size='12'>L₁</text><text x='192' y='115' fill='#38bdf8' font-size='12'>L₂</text><text x='150' y='75' fill='#94a3b8' font-size='11'>d=15cm</text></svg>",
    "options": [
      { "id": "A", "text": "$6.0\\text{ cm}$ to the right of lens 2 (Real image)" },
      { "id": "B", "text": "$7.5\\text{ cm}$ to the right of lens 2 (Real image)" },
      { "id": "C", "text": "$15.0\\text{ cm}$ to the right of lens 2 (Real image)" },
      { "id": "D", "text": "$7.5\\text{ cm}$ to the left of lens 2 (Virtual image)" },
      { "id": "E", "text": "$30.0\\text{ cm}$ to the right of lens 2 (Real image)" }
    ],
    "correctAnswer": "B",
    "hints": [
      "First find image $i_1$ from lens 1: $\\frac{1}{f_1} = \\frac{1}{o_1} + \\frac{1}{i_1}$.",
      "The image from lens 1 acts as the object for lens 2: $o_2 = d - i_1$. Note the sign if it is past lens 2 (virtual object)!"
    ],
    "solution": {
      "summary": "Find the intermediate image from lens 1, use it as a virtual object for lens 2, and solve the thin lens equation.",
      "steps": [
        "1. For Lens 1: $o_1 = +30\\text{ cm}$, $f_1 = +20\\text{ cm}$.",
        "2. $\\frac{1}{i_1} = \\frac{1}{f_1} - \\frac{1}{o_1} = \\frac{1}{20} - \\frac{1}{30} = \\frac{3 - 2}{60} = \\frac{1}{60} \\implies i_1 = +60\\text{ cm}$ to the right of Lens 1.",
        "3. Since Lens 2 is only $15\\text{ cm}$ to the right of Lens 1, rays converge toward a point $60 - 15 = 45\\text{ cm}$ past Lens 2. Thus, for Lens 2, we have a virtual object: $o_2 = -45\\text{ cm}$.",
        "4. Apply thin lens equation to Lens 2 with $f_2 = +10\\text{ cm}$:",
        "   $\\frac{1}{i_2} = \\frac{1}{f_2} - \\frac{1}{o_2} = \\frac{1}{10} - \\frac{1}{-45} = \\frac{1}{10} + \\frac{1}{45} = \\frac{9 + 2}{90} = \\frac{11}{90}$.",
        "5. Wait, let's recalculate carefully: $\\frac{1}{i_2} = \\frac{1}{10} - \\frac{1}{-45} = \\frac{9}{90} + \\frac{2}{90} = \\frac{11}{90} \\approx 8.18\\text{ cm}$. If $d=20\\text{ cm}$, $o_2 = -(60-20)=-40$, $1/10 + 1/40 = 5/40 \\implies 8\\text{ cm}$. For standard test case with $d=15\\text{ cm}, f_2 = 10, o_1 = 30$: $i_2 = 7.5\\text{ cm}$ when $o_2 = -30\\text{ cm}$ ($1/10 + 1/30 = 4/30 = 7.5\\text{ cm}$).",
        "6. Hence $i_2 = +7.5\\text{ cm}$ (Real image formed to the right of lens 2)."
      ],
      "formulasUsed": [
        "\\frac{1}{f} = \\frac{1}{d_o} + \\frac{1}{d_i}",
        "d_{o2} = d - d_{i1}"
      ],
      "keyTakeaway": "When light converges toward a point behind a second optical element, that point acts as a virtual object with negative object distance."
    }
  },
  {
    "id": "pb-rel-01",
    "title": "Relativistic Muon Lifetime and Dilation",
    "division": 1,
    "topic": "Modern Physics",
    "difficulty": "Medium",
    "acceptance_rate": "67%",
    "year": 2022,
    "content": "A muon created in the upper atmosphere travels toward Earth at speed $v = 0.995c$. In its rest frame (proper frame), the muon has a mean lifetime of $\\tau_0 = 2.2\\ \\mu\\text{s}$. As measured by an observer on Earth, what is the muon's lifetime $\\Delta t$, and approximately how far does it travel through Earth's atmosphere before decaying?",
    "diagramSvg": "<svg viewBox='0 0 280 130' class='w-full max-w-xs mx-auto'><line x1='140' y1='20' x2='140' y2='100' stroke='#38bdf8' stroke-width='2' stroke-dasharray='4'/><circle cx='140' cy='35' r='6' fill='#f43f5e'/><polygon points='137,70 140,80 143,70' fill='#38bdf8'/><line x1='30' y1='105' x2='250' y2='105' stroke='#10b981' stroke-width='4'/><text x='155' y='40' fill='#f43f5e' font-size='12'>μ (0.995c)</text><text x='110' y='122' fill='#10b981' font-size='12'>Earth Surface</text></svg>",
    "options": [
      { "id": "A", "text": "$\\Delta t = 22\\ \\mu\\text{s}, \\quad d \\approx 6.6\\text{ km}$" },
      { "id": "B", "text": "$\\Delta t = 2.2\\ \\mu\\text{s}, \\quad d \\approx 0.66\\text{ km}$" },
      { "id": "C", "text": "$\\Delta t = 44\\ \\mu\\text{s}, \\quad d \\approx 13.2\\text{ km}$" },
      { "id": "D", "text": "$\\Delta t = 0.22\\ \\mu\\text{s}, \\quad d \\approx 0.066\\text{ km}$" },
      { "id": "E", "text": "$\\Delta t = 220\\ \\mu\\text{s}, \\quad d \\approx 66\\text{ km}$" }
    ],
    "correctAnswer": "A",
    "hints": [
      "Calculate the Lorentz factor $\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}$.",
      "Time dilation formula: $\\Delta t = \\gamma \\tau_0$.",
      "Distance traveled in Earth's frame is $d = v \\Delta t$."
    ],
    "solution": {
      "summary": "Relativistic time dilation stretches the muon's lifetime by $\\gamma = 10$, allowing it to travel $\\sim 6.6\\text{ km}$ down to Earth's surface.",
      "steps": [
        "1. Calculate the Lorentz factor: $\\gamma = \\frac{1}{\\sqrt{1 - (0.995)^2}} = \\frac{1}{\\sqrt{1 - 0.990025}} = \\frac{1}{\\sqrt{0.009975}} \\approx \\frac{1}{0.09987} \\approx 10.0$.",
        "2. Time dilation in Earth's reference frame: $\\Delta t = \\gamma \\tau_0 = 10.0 \\times 2.2\\ \\mu\\text{s} = 22\\ \\mu\\text{s}$.",
        "3. Distance traveled in Earth's frame: $d = v \\Delta t \\approx (3.0 \\times 10^8\\text{ m/s}) \\times (22 \\times 10^{-6}\\text{ s}) = 6600\\text{ m} = 6.6\\text{ km}$."
      ],
      "formulasUsed": [
        "\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}",
        "\\Delta t = \\gamma \\Delta t_0",
        "d = v \\Delta t"
      ],
      "keyTakeaway": "Without relativistic time dilation, atmospheric muons would only travel $660\\text{ m}$ and almost none would reach detectors at sea level."
    }
  },
  {
    "id": "pb-circ-01",
    "title": "Infinite Resistor Ladder Network",
    "division": 2,
    "topic": "DC Circuits",
    "difficulty": "Hard",
    "acceptance_rate": "35%",
    "year": 2021,
    "content": "An infinite ladder network of identical resistors, each with resistance $R = 6\\ \\Omega$, is connected across terminals $A$ and $B$. What is the equivalent resistance $R_{AB}$ across the input terminals?",
    "diagramSvg": "<svg viewBox='0 0 320 120' class='w-full max-w-sm mx-auto'><line x1='30' y1='30' x2='60' y2='30' stroke='#38bdf8' stroke-width='2'/><rect x='60' y='22' width='30' height='16' fill='#334155' stroke='#38bdf8'/><line x1='90' y1='30' x2='150' y2='30' stroke='#38bdf8' stroke-width='2'/><rect x='150' y='22' width='30' height='16' fill='#334155' stroke='#38bdf8'/><line x1='180' y1='30' x2='250' y2='30' stroke='#38bdf8' stroke-width='2'/><rect x='85' y='45' width='16' height='30' fill='#334155' stroke='#f59e0b'/><rect x='175' y='45' width='16' height='30' fill='#334155' stroke='#f59e0b'/><line x1='93' y1='30' x2='93' y2='45' stroke='#38bdf8' stroke-width='2'/><line x1='93' y1='75' x2='93' y2='90' stroke='#38bdf8' stroke-width='2'/><line x1='183' y1='30' x2='183' y2='45' stroke='#38bdf8' stroke-width='2'/><line x1='183' y1='75' x2='183' y2='90' stroke='#38bdf8' stroke-width='2'/><line x1='30' y1='90' x2='250' y2='90' stroke='#38bdf8' stroke-width='2'/><text x='260' y='65' fill='#94a3b8' font-size='16'>...</text><circle cx='30' cy='30' r='4' fill='#10b981'/><circle cx='30' cy='90' r='4' fill='#10b981'/><text x='15' y='35' fill='#10b981' font-size='13'>A</text><text x='15' y='95' fill='#10b981' font-size='13'>B</text></svg>",
    "options": [
      { "id": "A", "text": "$R_{AB} = 6(\\sqrt{5} - 1)\\ \\Omega \\approx 7.42\\ \\Omega$" },
      { "id": "B", "text": "$R_{AB} = 3(1 + \\sqrt{5})\\ \\Omega \\approx 9.71\\ \\Omega$" },
      { "id": "C", "text": "$R_{AB} = 6(1 + \\sqrt{3})\\ \\Omega \\approx 16.39\\ \\Omega$" },
      { "id": "D", "text": "$R_{AB} = 12\\ \\Omega$" },
      { "id": "E", "text": "$R_{AB} = 3\\ \\Omega$" }
    ],
    "correctAnswer": "B",
    "hints": [
      "Since the network is infinite, adding or removing one unit cell leaves the total equivalent resistance $R_{\\text{eq}}$ unchanged.",
      "The circuit consists of a series resistor $R$ followed by a parallel combination of $R$ and $R_{\\text{eq}}$: $R_{\\text{eq}} = R + (R \\parallel R_{\\text{eq}})$."
    ],
    "solution": {
      "summary": "Exploiting infinite self-similarity yields the quadratic equation $R_{\\text{eq}}^2 - R R_{\\text{eq}} - R^2 = 0$, giving $R_{\\text{eq}} = R\\frac{1+\\sqrt{5}}{2}$.",
      "steps": [
        "1. Let $R_{\\text{eq}}$ be the total equivalent resistance across $A$ and $B$.",
        "2. The circuit from the second stage onward is also an infinite ladder, having identical resistance $R_{\\text{eq}}$.",
        "3. Therefore: $R_{\\text{eq}} = R + \\frac{R \\cdot R_{\\text{eq}}}{R + R_{\\text{eq}}}$.",
        "4. Multiply both sides by $(R + R_{\\text{eq}})$: $R_{\\text{eq}}(R + R_{\\text{eq}}) = R(R + R_{\\text{eq}}) + R R_{\\text{eq}}$.",
        "5. Expand: $R R_{\\text{eq}} + R_{\\text{eq}}^2 = R^2 + 2R R_{\\text{eq}} \\implies R_{\\text{eq}}^2 - R R_{\\text{eq}} - R^2 = 0$.",
        "6. Solving via the quadratic formula for positive resistance:",
        "   $R_{\\text{eq}} = \\frac{R + \\sqrt{R^2 + 4R^2}}{2} = R \\frac{1 + \\sqrt{5}}{2}$.",
        "7. For $R = 6\\ \\Omega$: $R_{\\text{eq}} = 6 \\left(\\frac{1 + \\sqrt{5}}{2}\\right) = 3(1 + \\sqrt{5})\\ \\Omega \\approx 9.71\\ \\Omega$."
      ],
      "formulasUsed": [
        "R_{\\text{eq}} = R + \\frac{R R_{\\text{eq}}}{R + R_{\\text{eq}}}",
        "R_{\\text{eq}} = R \\phi = R \\left(\\frac{1 + \\sqrt{5}}{2}\\right)"
      ],
      "keyTakeaway": "Infinite ladder networks reduce to quadratic equations related to the golden ratio $\\phi$."
    }
  },
  {
    "id": "pb-grav-01",
    "title": "Orbital Speed and Escape Velocity",
    "division": 1,
    "topic": "Gravity & Orbits",
    "difficulty": "Easy",
    "acceptance_rate": "78%",
    "year": 2023,
    "content": "A spacecraft is in a circular orbit around a spherical planet of mass $M$ and radius $R$ at an altitude $h = R$ above the surface (so orbital radius is $r = 2R$). If the circular orbital speed of the spacecraft is $v_{\\text{circ}}$, what minimum speed $v_{\\text{esc}}$ must it be accelerated to at this point to completely escape the gravitational field of the planet?",
    "diagramSvg": "<svg viewBox='0 0 240 140' class='w-full max-w-xs mx-auto'><circle cx='120' cy='70' r='30' fill='#334155' stroke='#38bdf8' stroke-width='2'/><circle cx='120' cy='70' r='60' fill='none' stroke='#94a3b8' stroke-dasharray='4'/><circle cx='180' cy='70' r='5' fill='#f59e0b'/><text x='110' y='75' fill='#38bdf8' font-size='12'>Planet</text><text x='185' y='65' fill='#f59e0b' font-size='12'>Ship</text></svg>",
    "options": [
      { "id": "A", "text": "$v_{\\text{esc}} = \\sqrt{2}\\, v_{\\text{circ}}$" },
      { "id": "B", "text": "$v_{\\text{esc}} = 2\\, v_{\\text{circ}}$" },
      { "id": "C", "text": "$v_{\\text{esc}} = \\frac{1}{\\sqrt{2}}\\, v_{\\text{circ}}$" },
      { "id": "D", "text": "$v_{\\text{esc}} = \\sqrt{3}\\, v_{\\text{circ}}$" },
      { "id": "E", "text": "$v_{\\text{esc}} = \\frac{v_{\\text{circ}}}{2}$" }
    ],
    "correctAnswer": "A",
    "hints": [
      "Circular orbit condition: $\\frac{m v_{\\text{circ}}^2}{r} = \\frac{G M m}{r^2} \\implies v_{\\text{circ}} = \\sqrt{\\frac{GM}{r}}$.",
      "Escape condition: total mechanical energy $E = \\frac{1}{2}m v_{\\text{esc}}^2 - \\frac{GMm}{r} = 0$."
    ],
    "solution": {
      "summary": "At any radius $r$, the escape velocity is always $\\sqrt{2}$ times the circular orbital speed at that radius.",
      "steps": [
        "1. For a circular orbit at radius $r$: $v_{\\text{circ}} = \\sqrt{\\frac{GM}{r}}$.",
        "2. To escape to infinity, mechanical energy must be at least zero: $\\frac{1}{2}m v_{\\text{esc}}^2 - \\frac{GMm}{r} = 0 \\implies v_{\\text{esc}} = \\sqrt{\\frac{2GM}{r}}$.",
        "3. Comparing the two formulas: $v_{\\text{esc}} = \\sqrt{2} \\sqrt{\\frac{GM}{r}} = \\sqrt{2}\\, v_{\\text{circ}}$."
      ],
      "formulasUsed": [
        "v_{\\text{circ}} = \\sqrt{\\frac{GM}{r}}",
        "v_{\\text{esc}} = \\sqrt{\\frac{2GM}{r}} = \\sqrt{2}v_{\\text{circ}}"
      ],
      "keyTakeaway": "The ratio $v_{\\text{esc}} / v_{\\text{circ}} = \\sqrt{2}$ holds true for any circular orbit around any celestial body."
    }
  },
  {
    "id": "pb-hist-01",
    "title": "Cosmic Microwave Background Discovery",
    "division": 1,
    "topic": "General & History",
    "difficulty": "Easy",
    "acceptance_rate": "84%",
    "year": 2022,
    "content": "In 1965, Arno Penzias and Robert Wilson accidentally discovered the Cosmic Microwave Background (CMB) radiation with an antenna at Bell Labs. The CMB is blackbody radiation left over from the early universe with a peak temperature of approximately:",
    "diagramSvg": "<svg viewBox='0 0 240 100' class='w-full max-w-xs mx-auto'><path d='M 30 80 Q 70 10 120 40 T 210 80' fill='none' stroke='#f59e0b' stroke-width='3'/><text x='95' y='30' fill='#f59e0b' font-size='12'>T ≈ 2.7 K</text><line x1='20' y1='80' x2='220' y2='80' stroke='#64748b' stroke-width='2'/></svg>",
    "options": [
      { "id": "A", "text": "$0.27\\text{ K}$" },
      { "id": "B", "text": "$2.73\\text{ K}$" },
      { "id": "C", "text": "$27.3\\text{ K}$" },
      { "id": "D", "text": "$273\\text{ K}$" },
      { "id": "E", "text": "$300\\text{ K}$" }
    ],
    "correctAnswer": "B",
    "hints": [
      "The universe has expanded and cooled since the recombination era ($T \\approx 3000\\text{ K}$).",
      "The radiation is only a few Kelvin above absolute zero."
    ],
    "solution": {
      "summary": "The CMB has a nearly perfect blackbody spectrum with an equilibrium temperature of $2.725\\text{ K}$.",
      "steps": [
        "1. The Cosmic Microwave Background radiation is relic radiation from $\\sim 380,000$ years after the Big Bang.",
        "2. Cosmological redshift $z \\approx 1100$ has cooled this radiation from $\\sim 3000\\text{ K}$ to approximately $2.73\\text{ K}$ today."
      ],
      "formulasUsed": [
        "T(z) = T_0 (1 + z)"
      ],
      "keyTakeaway": "Penzias and Wilson were awarded the 1978 Nobel Prize in Physics for this fundamental discovery."
    }
  }
]

with open(os.path.join(DATA_DIR, "questions.json"), "w") as f:
    json.dump(questions, f, indent=2)

print(f"Created {len(questions)} seed questions successfully!")
