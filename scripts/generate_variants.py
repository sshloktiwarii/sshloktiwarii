"""
Autonomous Design Foundry: 4 Radical Design Paradigms for Shlok Tiwari
Generates 4 distinct full-profile SVG concepts with ZERO copy-paste elements:

Variant 1: "LIQUID CHROME SPECULAR HUD" (Navy #070B14, Iridescent Chrome Mesh, Neon Olive Radar)
Variant 2: "SWISS INDUSTRIAL BRUTALISM" (Deep Obsidian, Swiss Hazard Amber #FFC32A, Precision Blueprint Grid)
Variant 3: "CYBER-TELEMETRY KINETIC TERMINAL" (CRT Scanlines, Emerald Oscilloscope #00FF9D, Live Kernel HUD)
Variant 4: "MINIMALIST LUXURY MONOCHROME" (Obsidian Slate #0A0D14, Platinum Specular Silver, High-End Editorial)
"""

import os
import math
import html

ROOT = "/Users/shloktiwari/Documents/untitled folder/completed projects/shloktiwari"
PREVIEWS = os.path.join(ROOT, "previews")
os.makedirs(PREVIEWS, exist_ok=True)

# -------------------------------------------------------------
# VARIANT 1: LIQUID CHROME SPECULAR HUD
# -------------------------------------------------------------
def make_v1():
    w, h = 1280, 820
    # Procedural liquid ribbons
    ribbons = []
    for r in range(8):
        pts = []
        for x in range(0, 1300, 30):
            y = 260 + math.sin(x * 0.008 + r * 0.6) * 45 + math.cos(x * 0.015 - r * 0.4) * 25 + r * 16
            pts.append(f"{x},{y:.1f}")
        ribbons.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#chrome_grad)" stroke-width="{2.4 - r*0.18:.2f}" opacity="{0.7 - r*0.06:.2f}"/>')
    
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
    <defs>
      <linearGradient id="chrome_grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#121A29"/>
        <stop offset="25%" stop-color="#8A98A8"/>
        <stop offset="50%" stop-color="#FFFFFF"/>
        <stop offset="75%" stop-color="#8A98A8"/>
        <stop offset="100%" stop-color="#121A29"/>
      </linearGradient>
      <linearGradient id="radar_glow" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#B4C97F" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="#8A9A5B" stop-opacity="0.1"/>
      </linearGradient>
      <filter id="bloom">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
    <style>
      .sweep {{ animation: sweep 4s linear infinite; transform-origin: 1100px 180px; }}
      @keyframes sweep {{ to {{ transform: rotate(360deg); }} }}
      .wave {{ animation: wave 6s ease-in-out infinite alternate; }}
      @keyframes wave {{ from {{ transform: translateY(-8px); }} to {{ transform: translateY(8px); }} }}
      .pulse {{ animation: p 2s ease-in-out infinite; }}
      @keyframes p {{ 0%,100% {{ opacity: 0.3; }} 50% {{ opacity: 0.9; }} }}
    </style>
    <rect width="{w}" height="{h}" fill="#070B14"/>
    
    <!-- Hero Bento Card -->
    <rect x="30" y="30" width="1220" height="340" rx="24" fill="#0D1424" stroke="#1E2A3E" stroke-width="1.5"/>
    <g class="wave">{"".join(ribbons)}</g>
    
    <!-- Radar Telemetry Widget -->
    <g transform="translate(1000, 80)">
      <circle cx="100" cy="100" r="80" fill="none" stroke="#1E2A3E" stroke-width="1.5"/>
      <circle cx="100" cy="100" r="55" fill="none" stroke="#1E2A3E" stroke-width="1.5" stroke-dasharray="4 4"/>
      <circle cx="100" cy="100" r="30" fill="none" stroke="#1E2A3E" stroke-width="1.5"/>
      <circle cx="100" cy="100" r="4" fill="#B4C97F" filter="url(#bloom)"/>
      <g class="sweep">
        <line x1="100" y1="100" x2="100" y2="20" stroke="#B4C97F" stroke-width="2" filter="url(#bloom)"/>
        <path d="M100 100 L100 20 A80 80 0 0 1 156 44 Z" fill="url(#radar_glow)"/>
      </g>
      <text x="100" y="205" text-anchor="middle" fill="#7E8C9F" font-family="monospace" font-size="11" letter-spacing="2">SYSTEM RADAR ACTIVE</text>
    </g>

    <!-- Hero Content -->
    <text x="70" y="90" fill="#B4C97F" font-family="monospace" font-size="14" font-weight="700" letter-spacing="3">// SYSTEM RUNTIME ARCHITECT</text>
    <text x="70" y="165" fill="#FFFFFF" font-family="system-ui, sans-serif" font-size="64" font-weight="900" letter-spacing="-1">SHLOK TIWARI</text>
    <text x="70" y="210" fill="#7E8C9F" font-family="monospace" font-size="18">Distributed AI Engines · Kernel Telemetry · Zero-Overhead Runtimes</text>
    
    <!-- Quick Specs -->
    <g transform="translate(70, 260)">
      <rect x="0" y="0" width="160" height="38" rx="8" fill="#121A2A" stroke="#25354D"/>
      <text x="80" y="24" text-anchor="middle" fill="#EAEFF7" font-family="monospace" font-size="13">RUST / C++</text>
      
      <rect x="175" y="0" width="160" height="38" rx="8" fill="#121A2A" stroke="#25354D"/>
      <text x="255" y="24" text-anchor="middle" fill="#EAEFF7" font-family="monospace" font-size="13">GO / PYTHON</text>

      <rect x="350" y="0" width="180" height="38" rx="8" fill="#121A2A" stroke="#25354D"/>
      <text x="440" y="24" text-anchor="middle" fill="#B4C97F" font-family="monospace" font-size="13">SUB-16MS WAL</text>
    </g>

    <!-- 6 Projects Row (2x3) -->
    <text x="30" y="415" fill="#EAEFF7" font-family="system-ui, sans-serif" font-size="24" font-weight="800">Flagship Systems</text>
    """
    
    projects = [
        ("SemCache", "AI Answer Cache & Vector Memory", "Python · Vector Cosine · Fast RTT", "#B4C97F"),
        ("AgentVault", "Deterministic Flight Recorder", "Rust · SQLite WAL · Telemetry", "#688836"),
        ("Sentinel-AI", "Unified Memory Runaway Tripwire", "C++ · Mach Microkernel · eBPF", "#B4C97F"),
        ("Aegis", "Kernel-Enforced Agent Sandbox", "Rust · Landlock · Apple Seatbelt", "#688836"),
        ("Strata", "Multi-Agent Fleet Orchestrator", "TypeScript · Distributed Runtime", "#B4C97F"),
        ("Cortex", "Cognitive Core & Agent Router", "Local LLMs · Task Routing", "#688836"),
    ]
    
    for i, (name, desc, stack, col) in enumerate(projects):
        row = i // 3
        col_idx = i % 3
        px = 30 + col_idx * 415
        py = 440 + row * 170
        body += f"""
        <g transform="translate({px}, {py})">
          <rect width="395" height="150" rx="16" fill="#0D1424" stroke="#1E2A3E" stroke-width="1.5"/>
          <circle cx="36" cy="36" r="14" fill="{col}" opacity="0.2"/>
          <circle cx="36" cy="36" r="6" fill="{col}"/>
          <text x="65" y="42" fill="#FFFFFF" font-family="system-ui, sans-serif" font-size="20" font-weight="700">{name}</text>
          <text x="25" y="82" fill="#A4B3C6" font-family="system-ui, sans-serif" font-size="14">{desc}</text>
          <text x="25" y="122" fill="#5F7085" font-family="monospace" font-size="12">{stack}</text>
        </g>
        """
    body += "</svg>"
    with open(os.path.join(PREVIEWS, "variant-1-liquid-chrome.svg"), "w") as f:
        f.write(body)

# -------------------------------------------------------------
# VARIANT 2: SWISS INDUSTRIAL BRUTALISM
# -------------------------------------------------------------
def make_v2():
    w, h = 1280, 820
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
    <defs>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1F1F1F" stroke-width="1"/>
      </pattern>
    </defs>
    <style>
      .blink {{ animation: bl 1s steps(1) infinite; }}
      @keyframes bl {{ 50% {{ opacity: 0; }} }}
    </style>
    <rect width="{w}" height="{h}" fill="#0A0A0A"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>

    <!-- Hero Blueprint Card -->
    <rect x="30" y="30" width="1220" height="330" fill="#111111" stroke="#333333" stroke-width="2"/>
    <rect x="30" y="30" width="1220" height="8" fill="#FFC32A"/>
    
    <text x="60" y="80" fill="#888888" font-family="monospace" font-size="13" letter-spacing="4">SPECIFICATION // REF: 2026-SYS</text>
    <text x="60" y="165" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="76" font-weight="900" letter-spacing="-2">SHLOK TIWARI</text>
    <text x="60" y="215" fill="#FFC32A" font-family="monospace" font-size="20" font-weight="700">HIGH-THROUGHPUT SYSTEMS &amp; DISTRIBUTED RUNTIMES</text>
    
    <!-- Blueprint Telemetry Data Box -->
    <g transform="translate(60, 255)">
      <rect x="0" y="0" width="1160" height="75" fill="#080808" stroke="#222222" stroke-width="1.5"/>
      <text x="30" y="32" fill="#666666" font-family="monospace" font-size="11">LATENCY TARGET</text>
      <text x="30" y="55" fill="#FFFFFF" font-family="monospace" font-size="16" font-weight="700">&lt; 16.0 MS</text>

      <text x="280" y="32" fill="#666666" font-family="monospace" font-size="11">DATABASE KERNEL</text>
      <text x="280" y="55" fill="#FFFFFF" font-family="monospace" font-size="16" font-weight="700">SQLITE WAL ENGINE</text>

      <text x="560" y="32" fill="#666666" font-family="monospace" font-size="11">CORE TOOLCHAIN</text>
      <text x="560" y="55" fill="#FFFFFF" font-family="monospace" font-size="16" font-weight="700">RUST / GO / C++</text>

      <text x="860" y="32" fill="#666666" font-family="monospace" font-size="11">ENGINEERING STATUS</text>
      <text x="860" y="55" fill="#FFC32A" font-family="monospace" font-size="16" font-weight="700">OPERATIONAL <tspan class="blink">_</tspan></text>
    </g>

    <!-- 6 Brutalist Grid Modules -->
    <text x="30" y="405" fill="#888888" font-family="monospace" font-size="13" letter-spacing="3">// DEPLOYED SUBSYSTEMS (06)</text>
    """
    
    projects = [
        ("01 // SEMCACHE", "Semantic AI Cache", "Remembers AI answers to save compute and eliminate repeat latency.", "PYTHON / VECTOR"),
        ("02 // AGENTVAULT", "Audit Flight Recorder", "Tamper-proof execution telemetry and black-box recorder for agents.", "RUST / SQLITE WAL"),
        ("03 // SENTINEL-AI", "Kernel Memory Tripwire", "Protects unified system memory against SSD swap death spirals.", "C++ / MACH KERNEL"),
        ("04 // AEGIS SANDBOX", "Deterministic Gateway", "Restricts autonomous agents from raw disk writes or key leaks.", "RUST / LANDLOCK"),
        ("05 // STRATA", "Fleet Orchestrator", "Dispatches and manages concurrent distributed agent workstreams.", "TYPESCRIPT / DISTRIBUTED"),
        ("06 // CORTEX", "Multi-Agent Brain", "Autonomous routing layer for decomposing large multi-domain tasks.", "LOCAL LLMS / ROUTER"),
    ]
    
    for i, (tag, name, desc, stack) in enumerate(projects):
        row = i // 3
        col_idx = i % 3
        px = 30 + col_idx * 415
        py = 430 + row * 175
        body += f"""
        <g transform="translate({px}, {py})">
          <rect width="395" height="155" fill="#111111" stroke="#2A2A2A" stroke-width="1.5"/>
          <rect width="4" height="155" fill="#FFC32A"/>
          <text x="25" y="32" fill="#FFC32A" font-family="monospace" font-size="12" font-weight="700">{tag}</text>
          <text x="25" y="62" fill="#FFFFFF" font-family="'Helvetica Neue', Arial, sans-serif" font-size="20" font-weight="800">{name}</text>
          <text x="25" y="92" fill="#999999" font-family="'Helvetica Neue', Arial, sans-serif" font-size="13">{desc[:55]}...</text>
          <text x="25" y="132" fill="#555555" font-family="monospace" font-size="11" font-weight="700">{stack}</text>
        </g>
        """
    body += "</svg>"
    with open(os.path.join(PREVIEWS, "variant-2-swiss-brutalism.svg"), "w") as f:
        f.write(body)

# -------------------------------------------------------------
# VARIANT 3: CYBER-TELEMETRY TERMINAL (CRT SCANLINES)
# -------------------------------------------------------------
def make_v3():
    w, h = 1280, 820
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
    <defs>
      <linearGradient id="scanline" x1="0" y1="0" x2="0" y2="100%">
        <stop offset="0%" stop-color="#000000" stop-opacity="0.3"/>
        <stop offset="50%" stop-color="#00FF9D" stop-opacity="0.03"/>
        <stop offset="100%" stop-color="#000000" stop-opacity="0.3"/>
      </linearGradient>
    </defs>
    <style>
      .glow {{ filter: drop-shadow(0 0 6px #00FF9D); }}
      .cursor {{ animation: blink 0.8s infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      .wave_osc {{ animation: osc 3s linear infinite; }}
      @keyframes osc {{ to {{ stroke-dashoffset: -200; }} }}
    </style>
    <rect width="{w}" height="{h}" fill="#050C08"/>
    
    <!-- Top Terminal Frame -->
    <rect x="30" y="30" width="1220" height="340" rx="16" fill="#07140D" stroke="#0D3823" stroke-width="2"/>
    
    <!-- Terminal Bar -->
    <rect x="30" y="30" width="1220" height="36" rx="16" fill="#0A1C12"/>
    <circle cx="55" cy="48" r="6" fill="#FF5F56"/>
    <circle cx="75" cy="48" r="6" fill="#FFBD2E"/>
    <circle cx="95" cy="48" r="6" fill="#27C93F"/>
    <text x="640" y="53" text-anchor="middle" fill="#00FF9D" font-family="monospace" font-size="12" opacity="0.6">shlok@distributed-node-01: ~ (kernel: aarch64-darwin)</text>

    <!-- Terminal Output -->
    <text x="60" y="105" fill="#00FF9D" font-family="monospace" font-size="14" opacity="0.7">$ whoami --verbose</text>
    <text x="60" y="165" fill="#FFFFFF" class="glow" font-family="monospace" font-size="54" font-weight="900">SHLOK TIWARI</text>
    <text x="60" y="210" fill="#00FF9D" font-family="monospace" font-size="18">> Systems Architect | Local-First AI Engines | eBPF &amp; Low Latency</text>
    
    <!-- Oscilloscope telemetry -->
    <g transform="translate(60, 240)">
      <path d="M 0 40 Q 50 10, 100 40 T 200 40 T 300 40 T 400 40 T 500 40 T 600 40 T 700 40 T 800 40" fill="none" stroke="#00FF9D" stroke-width="2.5" class="wave_osc glow" stroke-dasharray="16 8"/>
      <text x="0" y="80" fill="#4B8C6C" font-family="monospace" font-size="12">RUNTIME METRICS: 100% HEALTHY // 0.00% PACKET LOSS // 0 ZOMBIE NODES</text>
    </g>

    <!-- 6 Cyber Project Cards -->
    <text x="30" y="415" fill="#00FF9D" font-family="monospace" font-size="13">// SYSTEM REPOSITORIES [ONLINE: 6/6]</text>
    """
    
    projects = [
        ("SemCache", "Vector Cache Engine", "Zero-redundancy AI answer memory", "PYTHON / COSINE"),
        ("AgentVault", "Flight Recorder", "Cryptographic audit trail for agents", "RUST / WAL"),
        ("Sentinel-AI", "Mach Kernel Guard", "Sub-16ms Apple Silicon memory sentry", "C++ / EBPF"),
        ("Aegis", "Process Sandbox", "Confinement boundary against bad shell commands", "RUST / SEATBELT"),
        ("Strata", "Fleet Coordinator", "Multi-worker parallel orchestration loop", "TS / FLEET"),
        ("Cortex", "Cognitive Mesh", "Autonomous task-splitting router", "LOCAL LLM / ARCH"),
    ]
    
    for i, (name, role, desc, stack) in enumerate(projects):
        row = i // 3
        col_idx = i % 3
        px = 30 + col_idx * 415
        py = 440 + row * 170
        body += f"""
        <g transform="translate({px}, {py})">
          <rect width="395" height="150" rx="12" fill="#07140D" stroke="#0D3823" stroke-width="1.5"/>
          <text x="25" y="36" fill="#00FF9D" class="glow" font-family="monospace" font-size="18" font-weight="700">[{name}]</text>
          <text x="25" y="58" fill="#4B8C6C" font-family="monospace" font-size="11">{role}</text>
          <text x="25" y="92" fill="#C5E8D6" font-family="monospace" font-size="13">{desc}</text>
          <text x="25" y="128" fill="#00FF9D" font-family="monospace" font-size="11" opacity="0.8">> STACK: {stack}</text>
        </g>
        """
    body += "</svg>"
    with open(os.path.join(PREVIEWS, "variant-3-cyber-terminal.svg"), "w") as f:
        f.write(body)

# -------------------------------------------------------------
# VARIANT 4: MINIMALIST LUXURY MONOCHROME
# -------------------------------------------------------------
def make_v4():
    w, h = 1280, 820
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
    <rect width="{w}" height="{h}" fill="#0A0D14"/>
    
    <!-- Hero Card -->
    <rect x="30" y="30" width="1220" height="340" rx="28" fill="#101522" stroke="#1E273A" stroke-width="1.5"/>
    <text x="80" y="100" fill="#75859E" font-family="system-ui, sans-serif" font-size="13" font-weight="600" letter-spacing="4">SYSTEMS &amp; DISTRIBUTED ARCHITECTURE</text>
    <text x="80" y="180" fill="#FFFFFF" font-family="system-ui, sans-serif" font-size="72" font-weight="800" letter-spacing="-2">Shlok Tiwari</text>
    <text x="80" y="230" fill="#8E9EB5" font-family="system-ui, sans-serif" font-size="20">Crafting resilient, local-first computing engines and autonomous agent fleets.</text>
    
    <!-- Editorial Badges -->
    <g transform="translate(80, 280)">
      <text x="0" y="18" fill="#FFFFFF" font-family="monospace" font-size="14">C++ · Rust · Go · TypeScript · SQLite WAL</text>
    </g>

    <!-- 6 Refined Project Cards -->
    <text x="30" y="415" fill="#75859E" font-family="system-ui, sans-serif" font-size="14" font-weight="600" letter-spacing="2">FLAGSHIP PROJECTS</text>
    """
    
    projects = [
        ("SemCache", "Vector Answer Memory", "Instant responses for AI queries without redundant compute.", "Python / Cosine"),
        ("AgentVault", "Flight Recorder", "Tamper-proof execution telemetry and black-box recorder.", "Rust / SQLite WAL"),
        ("Sentinel-AI", "Unified Memory Sentry", "Protects Apple Silicon against swap spirals during LLM loads.", "C++ / Mach Kernel"),
        ("Aegis Sandbox", "Security Gateway", "Deterministic boundary against unsafe shell commands.", "Rust / Seatbelt"),
        ("Strata", "Fleet Control Center", "Coordinates multi-agent fleets across parallel workstreams.", "TypeScript / Fleet"),
        ("Cortex", "Cognitive Router", "Multi-agent dispatch core for complex distributed workflows.", "Local LLMs"),
    ]
    
    for i, (name, role, desc, stack) in enumerate(projects):
        row = i // 3
        col_idx = i % 3
        px = 30 + col_idx * 415
        py = 440 + row * 170
        body += f"""
        <g transform="translate({px}, {py})">
          <rect width="395" height="150" rx="20" fill="#101522" stroke="#1E273A" stroke-width="1.5"/>
          <text x="30" y="42" fill="#FFFFFF" font-family="system-ui, sans-serif" font-size="20" font-weight="700">{name}</text>
          <text x="30" y="66" fill="#6A7A91" font-family="system-ui, sans-serif" font-size="13">{role}</text>
          <text x="30" y="100" fill="#A3B2C7" font-family="system-ui, sans-serif" font-size="14">{desc}</text>
          <text x="30" y="130" fill="#4E5D73" font-family="monospace" font-size="12">{stack}</text>
        </g>
        """
    body += "</svg>"
    with open(os.path.join(PREVIEWS, "variant-4-minimal-luxury.svg"), "w") as f:
        f.write(body)

def main():
    make_v1()
    make_v2()
    make_v3()
    make_v4()
    print("All 4 design variants generated successfully in previews/!")

if __name__ == "__main__":
    main()
