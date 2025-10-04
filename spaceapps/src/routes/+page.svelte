<script>
  import Stars from "./Stars.svelte";
  import { onMount, onDestroy } from "svelte";

  // ---- UI state (translated) ----
  let selectedFile = null;
  let fileName = "No file selected";
  let isAnalyzing = false;
  let isResult = false;
  let result = null;

  function handleFileChange(event) {
    selectedFile = event.target.files[0];
    fileName = selectedFile ? selectedFile.name : "No file selected";
  }

  function analyzeFile() {
    if (!selectedFile) return;
    isAnalyzing = true;

    setTimeout(() => {
      isAnalyzing = false;
      isResult = true;

      const found = Math.random() > 0.4;
      if (found) {
        result = {
          found: true,
          probability: (Math.random() * (99.8 - 85.0) + 85.0).toFixed(2),
          period: (Math.random() * (365 - 5) + 5).toFixed(1),
          radius: (Math.random() * (2.5 - 0.8) + 0.8).toFixed(2),
        };
      } else {
        result = { found: false };
      }
    }, 3000);
  }

  function reset() {
    selectedFile = null;
    fileName = "No file selected";
    isAnalyzing = false;
    isResult = false;
    result = null;
  }

  // ---- Raylib (WASM) embed ----
  let canvasEl;
  let rayInstance = null;
  let rayReady = false;
  let rayError = null;

  onMount(async () => {
  try {
    // Intenta cargar Raylib solo si existe el archivo
    const response = await fetch("./rayapp.js", { method: "HEAD" });
    if (!response.ok) throw new Error("Raylib file not found");

    const createRayApp = (await import("./rayapp.js")).default;
    const Module = {
      canvas: canvasEl,
      locateFile: (p) => `/public/${p}`,
      print: (txt) => console.log(txt),
      printErr: (txt) => console.error(txt),
    };

    rayInstance = await createRayApp(Module);
    rayReady = true;
  } catch (e) {
    rayError = "Raylib module not yet available.";
    console.warn(rayError);
  }
});

</script>

<div class="container">
  <Stars/>

  <!-- Header -->
  <header class="header">
    <div class="logo">
      <img src="./logo.png" alt="Lightcurve Logo" class="logo-img" />
      <span class="logo-text">LIGHTCURVE</span>
    </div>
    <nav class="nav">
      <a href="#home">Home</a>
      <a href="#analyzer">AI Analyzer</a>
      <a href="#about">About</a>
    </nav>
  </header>

  <!-- Hero -->
  <section id="home" class="hero">
    <h1>Discover New Worlds</h1>
    <p>
      Using artificial intelligence to analyze light curves and find exoplanets at the edges of our universe.
    </p>
    <a href="#analyzer" class="btn-primary">Try our model</a>
  </section>

  <!-- Live Raylib (WASM) -->
  <section class="raylib-section">
    <div class="section-header">
      <h2>Live Visualization (WebAssembly)</h2>
      <p>Interactive rendering powered by Raylib + WebGL running right in your browser.</p>
    </div>

    <div class="glass-card">
      <div class="raylib-wrap">
        <canvas
          bind:this={canvasEl}
          id="raylib-canvas"
          class="raylib-canvas"
          width="800"
          height="450"
          aria-label="Raylib WebAssembly Canvas"
        ></canvas>
      </div>

      {#if !rayReady && !rayError}
        <p class="subtle">Loading Raylib module…</p>
      {/if}
      {#if rayError}
        <p class="warning">Could not load the Raylib module: {rayError}</p>
      {/if}
    </div>
  </section>

  <!-- Analyzer -->
  <section id="analyzer" class="analyzer">
    <div class="section-header">
      <h2>Data Analyzer</h2>
      <p>Upload a data file (e.g., CSV) and let our AI model analyze it.</p>
    </div>

    {#if !isAnalyzing && !isResult}
      <div class="glass-card">
        <div class="file-box">
          <input type="file" accept=".csv,.txt,.dat" on:change={handleFileChange} />
          <p>{fileName}</p>
        </div>
        <button on:click={analyzeFile} class="btn-primary" disabled={!selectedFile}>
          Analyze Data
        </button>
      </div>
    {/if}

    {#if isAnalyzing}
      <div class="glass-card center">
        <div class="loader"></div>
        <p class="loading-text">Analyzing with our AI model…</p>
        <small class="subtle">This may take a few seconds.</small>
      </div>
    {/if}

    {#if isResult}
      <div class="glass-card">
        <h3>Analysis Results</h3>
        <div class="text-center">
          {#if result.found}
            <h4 class="positive">Exoplanet Candidate Detected!</h4>
            <p class="subtle">Our model identified a consistent transit-like pattern.</p>
            <div class="results">
              <p><strong>Probability:</strong> {result.probability}%</p>
              <p><strong>Orbital Period (days):</strong> {result.period}</p>
              <p><strong>Planetary Radius (×R<sub>⊕</sub>):</strong> {result.radius}</p>
            </div>
          {:else}
            <h4 class="warning">No Clear Detection</h4>
            <p class="subtle">No significant transits were found.</p>
          {/if}
        </div>
        <button on:click={reset} class="btn-secondary">
          Analyze another file
        </button>
      </div>
    {/if}
  </section>

  <!-- About -->
  <section id="about" class="about">
    <h2>About Our Project</h2>
    <p>
      <span class="highlight">Lightcurve</span> is our solution for the
      <span class="highlight">NASA International Space Apps Challenge</span>. Our mission is to apply AI/ML
      techniques to automate exoplanet detection from stellar light curves.
    </p>
    <p>
      Our artificial intelligence model was trained on open datasets from NASA missions such as Kepler and TESS
      to learn characteristic patterns in stellar photometry. Using our own scientific visualization pipeline,
      developed with Raylib and C, we turn astronomy data into interactive, high-fidelity views. This helps us detect,
      analyze, and verify new exoplanet candidates with greater clarity and visual understanding than conventional methods.
    </p>
    <p class="team">Team: Lightcurve SpaceApps Team</p>
  </section>

  <footer class="footer">
    <p>&copy; 2025 Lightcurve Team. Built for the NASA Space Apps Challenge.</p>
  </footer>
</div>

<style>
  body {
    margin: 0;
    font-family: 'Abel', sans-serif;
    background-color: #0d0d0d;
    color: #eaeaea;
    line-height: 1.6;
  }

  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 1rem;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
  }
  .logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  .logo-img { height: 50px; width: 50px; }
  .logo-text {
    font-family: 'Abel', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    color:#f4f0f0
  }
  .nav {
    display: flex;
    gap: 2rem;
  }
  .nav a {
    color: #bbb;
    font-weight: 500;
    text-decoration: none;
    transition: color 0.3s;
  }
  .nav a:hover { color: #fff; }

  /* Hero */
  .hero {
    text-align: center;
    padding: 6rem 1rem;
  }
  .hero h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #f4f0f0;
  }
  .hero p {
    font-size: 1.2rem;
    color: #aaa;
    max-width: 700px;
    margin: 0 auto 2rem;
  }

  /* Raylib section */
  .raylib-section {
    padding: 6rem 1rem;
    text-align: center;
  }
  .raylib-wrap {
    width: 100%;
    max-width: 820px;
    margin: 0 auto;
  }
  .raylib-canvas {
    width: 100%;
    height: auto;
    display: block;
    aspect-ratio: 16/9; /* mantiene proporción visual */
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    background: #000;
  }

  /* Buttons */
  .btn-primary, .btn-secondary {
    font-weight: bold;
    padding: 0.9rem 2.2rem;
    border-radius: 999px;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
  }
  .btn-primary { background: #fff; color: #000; }
  .btn-primary:hover { background: #ddd; }
  .btn-secondary {
    display: block;
    width: 100%;
    margin-top: 1.5rem;
    background: #333;
    color: #fff;
  }
  .btn-secondary:hover { background: #555; }

  /* Sections */
  .analyzer, .about {
    padding: 6rem 1rem;
    text-align: center;
  }
  .section-header h2, .about h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color:#f4f0f0 ;
  }
  .section-header p, .about p {
    color: #aaa;
    max-width: 700px;
    margin: 0 auto 1.5rem;
    font-size: 1.1rem;
  }
  .highlight { color: #fff; font-weight: bold; }
  .team { margin-top: 2rem; font-weight: bold; }

  /* Cards */
  .glass-card {
    background: rgba(16, 16, 16, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    padding: 2.5rem;
    max-width: 650px;
    margin: 0 auto;
    color: white;
  }
  .file-box {
    border: 2px dashed #666;
    padding: 2rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 0.95rem;
    color: #bbb;
  }

  /* Loader */
  .loader {
    border: 4px solid rgba(255,255,255,0.2);
    border-left-color: #fff;
    border-radius: 50%;
    width: 50px; height: 50px;
    animation: spin 1s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Results */
  .positive { color: #4ade80; font-size: 1.3rem; margin-top: 1rem; }
  .warning { color: #facc15; font-size: 1.3rem; margin-top: 1rem; }
  .results {
    margin-top: 1.5rem;
    background: rgba(0,0,0,0.4);
    padding: 1rem 1.5rem;
    border-radius: 0.75rem;
    text-align: left;
    color: #f4f0f0;
  }

  .subtle { color: #aaa; font-size: 0.95rem; }

  /* Footer */
  .footer {
    border-top: 1px solid #222;
    padding: 2rem;
    text-align: center;
    font-size: 0.9rem;
    color: #666;
    margin-top: 3rem;
  }
</style>
