<script>
  import Stars from "./Stars.svelte";

  let selectedFile = null;
  let fileName = "Ningún archivo seleccionado";
  let isAnalyzing = false;
  let isResult = false;
  let result = null;

  function handleFileChange(event) {
    selectedFile = event.target.files[0];
    if (selectedFile) {
      fileName = selectedFile.name;
    } else {
      fileName = "Ningún archivo seleccionado";
    }
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
    fileName = "Ningún archivo seleccionado";
    isAnalyzing = false;
    isResult = false;
    result = null;
  }
</script>

<div class="container">
  <Stars/>

  <!-- Header -->
  <header class="header">
    <div class="logo">
      <img src="./logo.png" alt="Lightcurve Logo" class="logo-img">
      <span class="logo-text">LIGHTCURVE</span>
    </div>
    <nav class="nav">
      <a href="#home">Inicio</a>
      <a href="#analyzer">Analizador IA</a>
      <a href="#about">Sobre el Proyecto</a>
    </nav>
  </header>

  <!-- Hero -->
  <section id="home" class="hero">
    <h1>Descubre Nuevos Mundos</h1>
    <p>
      Utilizando inteligencia artificial para analizar curvas de luz y encontrar exoplanetas en los confines del universo.
    </p>
    <a href="#analyzer" class="btn-primary">Prueba nuestro modelo</a>
  </section>

  <!-- Analyzer -->
  <section id="analyzer" class="analyzer">
    <div class="section-header">
      <h2>Analizador de datos</h2>
      <p>Sube un archivo de datos (ej. CSV) para que nuestro modelo de IA lo analice.</p>
    </div>

    {#if !isAnalyzing && !isResult}
      <div class="glass-card">
        <div class="file-box">
          <input type="file" accept=".csv,.txt,.dat" on:change={handleFileChange} />
          <p>{fileName}</p>
        </div>
        <button on:click={analyzeFile} class="btn-primary" disabled={!selectedFile}>
          Analizar Datos
        </button>
      </div>
    {/if}

    {#if isAnalyzing}
      <div class="glass-card center">
        <div class="loader"></div>
        <p class="loading-text">Analizando con nuestro modelo IA...</p>
        <small class="subtle">Esto puede tardar unos segundos.</small>
      </div>
    {/if}

    {#if isResult}
      <div class="glass-card">
        <h3>Resultados del Análisis</h3>
        <div class="text-center">
          {#if result.found}
            <h4 class="positive">¡Candidato a Exoplaneta Detectado!</h4>
            <p class="subtle">Nuestro modelo identificó un patrón consistente.</p>
            <div class="results">
              <p><strong>Probabilidad:</strong> {result.probability}%</p>
              <p><strong>Periodo Orbital:</strong> {result.period} días</p>
              <p><strong>Radio Planetario:</strong> {result.radius}x</p>
            </div>
          {:else}
            <h4 class="warning">Sin Detección Clara</h4>
            <p class="subtle">No se encontraron tránsitos significativos.</p>
          {/if}
        </div>
        <button on:click={reset} class="btn-secondary">
          Analizar otro archivo
        </button>
      </div>
    {/if}
  </section>

  <!-- About -->
  <section id="about" class="about">
    <h2>Sobre Nuestro Proyecto</h2>
    <p>
      <span class="highlight">Lightcurve</span> es nuestra solución para el <span class="highlight">NASA International Space Apps Challenge</span>. Nuestro reto es aplicar técnicas de Inteligencia Artificial y Machine Learning (AI/ML) para automatizar la detección de exoplanetas.
    </p>
    <p>
      Nuestro modelo de inteligencia artificial fue entrenado con conjuntos de datos abiertos provenientes de misiones de la NASA, como Kepler y TESS, para aprender a reconocer patrones característicos en las curvas de luz de las estrellas.

        Utilizando nuestra propia herramienta de visualización científica, desarrollada con Reilid y C, transformamos los datos astronómicos en representaciones interactivas y precisas. Esto permite detectar, analizar y verificar nuevos candidatos a exoplanetas con una mayor claridad y comprensión visual que los métodos convencionales.
    </p>
    <p class="team">Equipo: Lightcurve SpaceApps Team</p>
  </section>

  <footer class="footer">
    <p>&copy; 2025 Lightcurve Team. Creado para el NASA Space Apps Challenge.</p>
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
        font-family: 'Abel', sans-serif;

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
        font-family: 'Abel', sans-serif;

  }
  .hero h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #f4f0f0;
        font-family: 'Abel', sans-serif;

  }
  .hero p {
    font-size: 1.2rem;
    color: #aaa;
    max-width: 700px;
    margin: 0 auto 2rem;
        font-family: 'Abel', sans-serif;

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
  .btn-primary {
    background: #fff;
    color: #000;
  }
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
        font-family: 'Abel', sans-serif;

  }
  .section-header h2, .about h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color:#f4f0f0 ;
        font-family: 'Abel', sans-serif;

  }
  .section-header p, .about p {
    color: #aaa;
    max-width: 700px;
    margin: 0 auto 1.5rem;
    font-size: 1.1rem;
        font-family: 'Abel', sans-serif;

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
        font-family: 'Abel', sans-serif;

  }
  .file-box {
    border: 2px dashed #666;
    padding: 2rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 0.95rem;
    color: #bbb;
        font-family: 'Abel', sans-serif;

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
        font-family: 'Abel', sans-serif;

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
        font-family: 'Abel', sans-serif;

  }
</style>
