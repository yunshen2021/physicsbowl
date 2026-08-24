import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

formulas_data = {
  "constants": [
    { "name": "Speed of Light in Vacuum", "symbol": "c", "value": "3.00 \\times 10^8", "unit": "\\text{m/s}" },
    { "name": "Planck's Constant", "symbol": "h", "value": "6.63 \\times 10^{-34}", "unit": "\\text{J}\\cdot\\text{s} = 4.14 \\times 10^{-15} \\text{ eV}\\cdot\\text{s}" },
    { "name": "Reduced Planck Constant", "symbol": "\\hbar", "value": "1.05 \\times 10^{-34}", "unit": "\\text{J}\\cdot\\text{s}" },
    { "name": "Gravitational Constant", "symbol": "G", "value": "6.67 \\times 10^{-11}", "unit": "\\text{N}\\cdot\\text{m}^2/\\text{kg}^2" },
    { "name": "Acceleration due to Gravity", "symbol": "g", "value": "9.80", "unit": "\\text{m/s}^2" },
    { "name": "Elementary Charge", "symbol": "e", "value": "1.60 \\times 10^{-19}", "unit": "\\text{C}" },
    { "name": "Electron Mass", "symbol": "m_e", "value": "9.11 \\times 10^{-31}", "unit": "\\text{kg} = 0.511 \\text{ MeV}/c^2" },
    { "name": "Proton Mass", "symbol": "m_p", "value": "1.673 \\times 10^{-27}", "unit": "\\text{kg} = 938.3 \\text{ MeV}/c^2" },
    { "name": "Permittivity of Free Space", "symbol": "\\epsilon_0", "value": "8.85 \\times 10^{-12}", "unit": "\\text{C}^2/(\\text{N}\\cdot\\text{m}^2)" },
    { "name": "Coulomb Constant", "symbol": "k = \\frac{1}{4\\pi\\epsilon_0}", "value": "8.99 \\times 10^9", "unit": "\\text{N}\\cdot\\text{m}^2/\\text{C}^2" },
    { "name": "Permeability of Free Space", "symbol": "\\mu_0", "value": "4\\pi \\times 10^{-7}", "unit": "\\text{T}\\cdot\\text{m}/\\text{A}" },
    { "name": "Boltzmann Constant", "symbol": "k_B", "value": "1.38 \\times 10^{-23}", "unit": "\\text{J/K}" },
    { "name": "Universal Gas Constant", "symbol": "R", "value": "8.314", "unit": "\\text{J}/(\\text{mol}\\cdot\\text{K})" },
    { "name": "Avogadro's Number", "symbol": "N_A", "value": "6.02 \\times 10^{23}", "unit": "\\text{mol}^{-1}" },
    { "name": "Standard Atmospheric Pressure", "symbol": "1\\text{ atm}", "value": "1.013 \\times 10^5", "unit": "\\text{Pa}" }
  ],
  "categories": [
    {
      "category": "Mechanics",
      "formulas": [
        { "title": "Kinematic Equations (Constant a)", "latex": "v = v_0 + at, \\quad x = x_0 + v_0 t + \\frac{1}{2}at^2, \\quad v^2 = v_0^2 + 2a(x - x_0)" },
        { "title": "Newton's 2nd Law & Momentum", "latex": "\\vec{F}_{\\text{net}} = m\\vec{a} = \\frac{d\\vec{p}}{dt}, \\quad \\vec{J} = \\int \\vec{F}\\,dt = \\Delta\\vec{p}" },
        { "title": "Work & Kinetic Energy", "latex": "W = \\int \\vec{F}\\cdot d\\vec{r} = \\Delta K, \\quad K = \\frac{1}{2}mv^2, \\quad P = \\frac{dW}{dt} = \\vec{F}\\cdot\\vec{v}" },
        { "title": "Universal Gravitation & Orbits", "latex": "F_g = \\frac{G M m}{r^2}, \\quad U_g = -\\frac{G M m}{r}, \\quad v_{\\text{orbit}} = \\sqrt{\\frac{GM}{r}}, \\quad v_{\\text{esc}} = \\sqrt{\\frac{2GM}{r}}" },
        { "title": "Rotational Motion", "latex": "\\omega = \\omega_0 + \\alpha t, \\quad \\tau = I\\alpha, \\quad L = I\\omega = \\vec{r}\\times\\vec{p}, \\quad K_{\\text{rot}} = \\frac{1}{2}I\\omega^2" },
        { "title": "Simple Harmonic Motion", "latex": "T = 2\\pi\\sqrt{\\frac{m}{k}}, \\quad T_{\\text{pendulum}} = 2\\pi\\sqrt{\\frac{L}{g}}, \\quad \\omega = 2\\pi f = \\sqrt{\\frac{k}{m}}" }
      ]
    },
    {
      "category": "Thermodynamics & Fluids",
      "formulas": [
        { "title": "Ideal Gas Law & Kinetic Energy", "latex": "PV = nRT = N k_B T, \\quad K_{\\text{avg}} = \\frac{3}{2}k_B T, \\quad v_{\\text{rms}} = \\sqrt{\\frac{3k_B T}{m}}" },
        { "title": "First Law & Heat Engines", "latex": "\\Delta U = Q - W, \\quad W_{\\text{isothermal}} = nRT\\ln\\left(\\frac{V_f}{V_i}\\right), \\quad e_{\\text{Carnot}} = 1 - \\frac{T_C}{T_H}" },
        { "title": "Fluid Dynamics", "latex": "P = P_0 + \\rho gh, \\quad F_{\\text{buoyant}} = \\rho_{\\text{fluid}} V_{\\text{submerged}} g, \\quad A_1 v_1 = A_2 v_2" }
      ]
    },
    {
      "category": "Electricity & Magnetism",
      "formulas": [
        { "title": "Electrostatics & Potential", "latex": "F_e = \\frac{k|q_1 q_2|}{r^2}, \\quad \\vec{E} = \\frac{\\vec{F}}{q}, \\quad V = \\frac{kq}{r}, \\quad U = \\frac{k q_1 q_2}{r}" },
        { "title": "Capacitors & Circuits", "latex": "C = \\frac{Q}{V} = \\frac{\\kappa \\epsilon_0 A}{d}, \\quad U_C = \\frac{1}{2}CV^2, \\quad V = IR, \\quad P = IV = I^2 R" },
        { "title": "Magnetic Forces & Induction", "latex": "\\vec{F}_B = q(\\vec{v}\\times\\vec{B}), \\quad \\vec{F}_B = I(\\vec{L}\\times\\vec{B}), \\quad \\Phi_B = \\int \\vec{B}\\cdot d\\vec{A}, \\quad \\mathcal{E} = -\\frac{d\\Phi_B}{dt}" }
      ]
    },
    {
      "category": "Waves, Optics & Modern",
      "formulas": [
        { "title": "Waves & Sound", "latex": "v = f\\lambda, \\quad f' = f\\left(\\frac{v \\pm v_o}{v \\mp v_s}\\right), \\quad d\\sin\\theta = m\\lambda" },
        { "title": "Geometric Optics", "latex": "n_1\\sin\\theta_1 = n_2\\sin\\theta_2, \\quad \\frac{1}{f} = \\frac{1}{d_o} + \\frac{1}{d_i}, \\quad M = -\\frac{d_i}{d_o}" },
        { "title": "Quantum & Relativity", "latex": "E = hf = \\frac{hc}{\\lambda}, \\quad K_{\\text{max}} = hf - \\Phi, \\quad \\lambda = \\frac{h}{p}, \\quad \\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}, \\quad E = \\gamma mc^2" }
      ]
    }
  ]
}

with open(os.path.join(DATA_DIR, "formulas.json"), "w") as f:
    json.dump(formulas_data, f, indent=2)

print("Created formulas.json successfully!")
