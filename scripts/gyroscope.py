"""
Procedural 3D Orbital Rings / Elliptical Gyroscope Background
Kinetic multi-axis spinning gimbal and planetary orbits.
"""

def gyroscope_mesh(cx=620, cy=200, color="#8A9A5B", glow="#B4C97F", opacity=0.45):
    return f"""
    <g class="gyro_group" opacity="{opacity}">
      <!-- Outer Orbit Ring -->
      <ellipse cx="{cx}" cy="{cy}" rx="320" ry="120" fill="none" stroke="{color}" stroke-width="1.8" stroke-dasharray="12 8" class="ring_orbit_1"/>
      
      <!-- Angled Orbit Ring 2 -->
      <g transform="rotate(35 {cx} {cy})">
        <ellipse cx="{cx}" cy="{cy}" rx="280" ry="90" fill="none" stroke="{glow}" stroke-width="1.4" class="ring_orbit_2"/>
        <circle cx="{cx + 280}" cy="{cy}" r="4.5" fill="{glow}"/>
      </g>
      
      <!-- Angled Orbit Ring 3 -->
      <g transform="rotate(-40 {cx} {cy})">
        <ellipse cx="{cx}" cy="{cy}" rx="240" ry="75" fill="none" stroke="{color}" stroke-width="1.5" stroke-dasharray="8 6" class="ring_orbit_3"/>
        <circle cx="{cx - 240}" cy="{cy}" r="4" fill="{color}"/>
      </g>
      
      <!-- Core Telemetry Concentrics -->
      <circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{color}" stroke-width="1" stroke-dasharray="4 6"/>
      <circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{glow}" stroke-width="1.2"/>
      <circle cx="{cx}" cy="{cy}" r="5" fill="{glow}"/>
    </g>
    """

GYRO_CSS = """
.ring_orbit_1 {
  animation: gyro_spin_1 24s linear infinite;
  transform-origin: 620px 200px;
}
@keyframes gyro_spin_1 {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.ring_orbit_2 {
  animation: gyro_spin_2 18s linear infinite reverse;
  transform-origin: 620px 200px;
}
@keyframes gyro_spin_2 {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.ring_orbit_3 {
  animation: gyro_spin_3 22s linear infinite;
  transform-origin: 620px 200px;
}
@keyframes gyro_spin_3 {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
"""
