"""
Custom Animated Cyber Visor Robot Avatar for Shlok Tiwari
A bespoke, futuristic cyborg/mecha head with an animated scanning visor and glowing antennae.
Zero resemblance to the harsh4k hand-drawn boy avatar.
"""

def cyber_avatar(x, y, size, accent="#8A9A5B", glow="#B4C97F", bg="#070B14"):
    return f"""
    <g class="cyber_bob" transform="translate({x}, {y}) scale({size / 100:.3f})">
      <!-- Outer Hex/Circle Shield -->
      <circle cx="50" cy="50" r="46" fill="{bg}" stroke="{accent}" stroke-width="2.5" opacity="0.9"/>
      <circle cx="50" cy="50" r="42" fill="none" stroke="{accent}" stroke-width="1" stroke-dasharray="4 6" opacity="0.4"/>
      
      <!-- Head Base Chassis -->
      <path d="M26 34 L32 20 L68 20 L74 34 L72 68 L50 82 L28 68 Z" fill="#0E1726" stroke="{accent}" stroke-width="2"/>
      
      <!-- Ear Audio Sensors / Nodes -->
      <rect x="20" y="42" width="7" height="18" rx="3" fill="{accent}"/>
      <rect x="73" y="42" width="7" height="18" rx="3" fill="{accent}"/>
      
      <!-- Top Antenna Beacon with Pulse -->
      <line x1="50" y1="20" x2="50" y2="10" stroke="{accent}" stroke-width="2"/>
      <circle cx="50" cy="8" r="3.5" fill="{glow}" class="beacon_pulse"/>
      
      <!-- Cyber Visor Window -->
      <path d="M30 40 L70 40 L68 56 L32 56 Z" fill="#060C16" stroke="{glow}" stroke-width="1.5"/>
      
      <!-- Glowing Animated Visor Laser Scan Bar -->
      <g clip-path="url(#visor_clip)">
        <rect x="30" y="44" width="14" height="8" rx="3" fill="{glow}" class="visor_scan"/>
      </g>
      
      <!-- Mouth Grill / Tactical Ports -->
      <line x1="40" y1="68" x2="60" y2="68" stroke="{accent}" stroke-width="1.8" opacity="0.7"/>
      <line x1="44" y1="73" x2="56" y2="73" stroke="{accent}" stroke-width="1.8" opacity="0.7"/>
    </g>
    """

CYBER_CSS = """
.cyber_bob {
  animation: cyber_float 4s ease-in-out infinite;
  transform-origin: center;
}
@keyframes cyber_float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
.visor_scan {
  animation: scan 2.6s ease-in-out infinite alternate;
}
@keyframes scan {
  from { transform: translateX(0); }
  to { transform: translateX(26px); }
}
.beacon_pulse {
  animation: beacon 1.4s ease-in-out infinite alternate;
}
@keyframes beacon {
  from { opacity: 0.3; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1.3); }
}
"""
