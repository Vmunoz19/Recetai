// Ingredient Recognition JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Botón de generar receta con IA
  const generateBtn = document.getElementById("generateRecipeBtn");
  const generatedRecipeCard = document.getElementById("generatedRecipeCard");
  const aiGenerateCard = document.getElementById("aiGenerateCard");

  if (generateBtn) {
    generateBtn.addEventListener("click", function () {
      // Aquí iría la lógica real de generación con IA
      console.log("Generando receta con IA...");

      // Simular loading
      const originalText = generateBtn.innerHTML;
      generateBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Generando...';
      generateBtn.disabled = true;

      setTimeout(() => {
        // Ocultar la card de generación
        if (aiGenerateCard) {
          aiGenerateCard.style.transition = "all 0.3s ease";
          aiGenerateCard.style.opacity = "0";
          aiGenerateCard.style.transform = "scale(0.95)";

          setTimeout(() => {
            aiGenerateCard.style.display = "none";

            // Mostrar la card de receta generada en su lugar
            if (generatedRecipeCard) {
              generatedRecipeCard.style.display = "flex";
              generatedRecipeCard.style.opacity = "0";
              generatedRecipeCard.style.transform = "scale(0.95)";

              setTimeout(() => {
                generatedRecipeCard.style.transition = "all 0.4s ease";
                generatedRecipeCard.style.opacity = "1";
                generatedRecipeCard.style.transform = "scale(1)";
              }, 10);
            }
          }, 300);
        }
      }, 2000);
    });
  }

  // Botón de volver a generar
  const regenerateBtn = document.getElementById("regenerateRecipeBtn");
  if (regenerateBtn) {
    regenerateBtn.addEventListener("click", function () {
      if (generatedRecipeCard && aiGenerateCard) {
        // Ocultar la receta actual
        generatedRecipeCard.style.transition = "all 0.3s ease";
        generatedRecipeCard.style.opacity = "0";
        generatedRecipeCard.style.transform = "scale(0.95)";

        setTimeout(() => {
          generatedRecipeCard.style.display = "none";
          generatedRecipeCard.style.transform = "scale(1)";

          // Mostrar la card de generación
          aiGenerateCard.style.display = "flex";
          aiGenerateCard.style.opacity = "0";
          aiGenerateCard.style.transform = "scale(0.95)";

          setTimeout(() => {
            aiGenerateCard.style.transition = "all 0.3s ease";
            aiGenerateCard.style.opacity = "1";
            aiGenerateCard.style.transform = "scale(1)";

            // Auto-click en el botón de generar después de mostrar la card
            setTimeout(() => {
              if (generateBtn) {
                generateBtn.click();
              }
            }, 400);
          }, 10);
        }, 300);
      }
    });
  }

  // Botón de cerrar receta generada
  const closeGeneratedRecipeBtn = document.getElementById(
    "closeGeneratedRecipe"
  );
  if (closeGeneratedRecipeBtn) {
    closeGeneratedRecipeBtn.addEventListener("click", function () {
      if (generatedRecipeCard && aiGenerateCard) {
        // Ocultar la receta generada
        generatedRecipeCard.style.transition = "all 0.3s ease";
        generatedRecipeCard.style.opacity = "0";
        generatedRecipeCard.style.transform = "scale(0.95)";

        setTimeout(() => {
          generatedRecipeCard.style.display = "none";
          generatedRecipeCard.style.transform = "scale(1)";

          // Mostrar nuevamente la card de generación
          aiGenerateCard.style.display = "flex";
          aiGenerateCard.style.opacity = "0";
          aiGenerateCard.style.transform = "scale(0.95)";

          setTimeout(() => {
            aiGenerateCard.style.transition = "all 0.3s ease";
            aiGenerateCard.style.opacity = "1";
            aiGenerateCard.style.transform = "scale(1)";
          }, 10);
        }, 300);
      }
    });
  }

  // Animación de entrada para las cards
  const animateCards = () => {
    const cards = document.querySelectorAll(".recipe-card");
    cards.forEach((card, index) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(20px)";

      setTimeout(() => {
        card.style.transition = "all 0.4s ease";
        card.style.opacity = "1";
        card.style.transform = "translateY(0)";
      }, index * 100);
    });
  };

  // Ejecutar animación si hay cards
  if (document.querySelectorAll(".recipe-card").length > 0) {
    animateCards();
  }

  // Animación de los ingredientes detectados
  const animateIngredients = () => {
    const ingredients = document.querySelectorAll(".ingredient-item");
    ingredients.forEach((ingredient, index) => {
      ingredient.style.opacity = "0";
      ingredient.style.transform = "translateX(-20px)";

      setTimeout(() => {
        ingredient.style.transition = "all 0.3s ease";
        ingredient.style.opacity = "1";
        ingredient.style.transform = "translateX(0)";
      }, index * 50);
    });
  };

  if (document.querySelectorAll(".ingredient-item").length > 0) {
    animateIngredients();
  }

  // Botón de guardar en favoritos
  const favoriteBtns = document.querySelectorAll(".btn-favorite");
  favoriteBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const icon = this.querySelector("i");

      if (icon.classList.contains("far")) {
        // Añadir a favoritos
        icon.classList.remove("far");
        icon.classList.add("fas");
        this.innerHTML = '<i class="fas fa-star"></i> Guardado en Favoritos';

        // Aquí iría la lógica real de guardar en favoritos
        console.log("Receta guardada en favoritos");
      } else {
        // Quitar de favoritos
        icon.classList.remove("fas");
        icon.classList.add("far");
        this.innerHTML = '<i class="far fa-star"></i> Guardar en Favoritos';

        console.log("Receta removida de favoritos");
      }
    });
  });

  // Smooth scroll para la lista de ingredientes y recetas
  const scrollContainers = document.querySelectorAll(
    ".ingredients-list, .recipes-list, .generated-recipe-card"
  );
  scrollContainers.forEach((container) => {
    let isDown = false;
    let startY;
    let scrollTop;

    container.addEventListener("mousedown", (e) => {
      if (e.target.tagName === "A" || e.target.closest("a")) return;
      isDown = true;
      container.style.cursor = "grabbing";
      startY = e.pageY - container.offsetTop;
      scrollTop = container.scrollTop;
    });

    container.addEventListener("mouseleave", () => {
      isDown = false;
      container.style.cursor = "default";
    });

    container.addEventListener("mouseup", () => {
      isDown = false;
      container.style.cursor = "default";
    });

    container.addEventListener("mousemove", (e) => {
      if (!isDown) return;
      e.preventDefault();
      const y = e.pageY - container.offsetTop;
      const walk = (y - startY) * 2;
      container.scrollTop = scrollTop - walk;
    });
  });
});

// Función para simular el escaneo (para futuras implementaciones)
function simulateScan() {
  console.log("Iniciando escaneo...");
  // Aquí iría la lógica de captura de imagen y análisis con IA
}

// Función para procesar imagen subida (para futuras implementaciones)
function processUploadedImage(file) {
  console.log("Procesando imagen:", file.name);
  // Aquí iría la lógica de procesamiento de imagen con IA
}

// Exportar funciones para uso global
window.ingredientRecognition = {
  simulateScan,
  processUploadedImage,
};

/* ---- Nueva lógica: captura desde la cámara y envío al servidor ---- */
async function sendFrameToServer(blob) {
  const fd = new FormData();
  fd.append('image', blob, 'frame.jpg');

  const csrftoken = (function(){
    const v = `; ${document.cookie}`.split(`; csrftoken=`);
    if (v.length===2) return v.pop().split(';').shift();
    return null;
  })();

  const res = await fetch('/ingredients/api/detect/', {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: fd
  });
  if (!res.ok) {
    let body = null;
    try {
      body = await res.json();
    } catch (e) {
      try { body = await res.text(); } catch (e2) { body = null; }
    }
    console.error('Server returned', res.status, body);
    return null;
  }
  try {
    return await res.json();
  } catch (e) {
    console.error('Invalid JSON from detect API', e);
    return null;
  }
}

function startCameraScan() {
  const startBtn = document.getElementById('startScannerBtn');
  const stopBtn = document.getElementById('stopScannerBtn');
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  const preview = document.querySelector('.camera-preview');

  let stream = null;
  let intervalId = null;
  let isRequesting = false; // evita solapamiento de requests
  let frozen = false; // cuando el usuario detiene, results se "congelan"

  async function start() {
    try {
      console.log('[scanner] start() called - requesting camera');
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
      console.log('[scanner] getUserMedia succeeded', stream);
      video.srcObject = stream;
      // try to ensure playback starts
      try { await video.play(); } catch (e) { /* autoplay may be blocked */ }
      preview.style.display = '';
      console.log('[scanner] preview displayed');
      startBtn.disabled = true;
      stopBtn.disabled = false;

      const ctx = canvas.getContext('2d');

      const CAPTURE_INTERVAL = 1500; // ms, puede ajustarse

      async function captureAndSend() {
        try {
          if (isRequesting) return; // ya hay una petición en curso
          if (!video.videoWidth || !video.videoHeight) return;
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          isRequesting = true;
          // compress to jpeg and send
          console.log('[scanner] sending frame', { time: new Date().toISOString() });
          canvas.toBlob(async (blob) => {
            if (!blob) { isRequesting = false; return; }
            const data = await sendFrameToServer(blob);
            isRequesting = false;
            if (!data) {
              console.warn('[scanner] detect API returned no data');
              return;
            }
            // Debug: log raw detection response so the developer can inspect structure
            console.log('[scanner] detection response', data);
            if (!frozen) {
              updateDetectionUI(data);
              updateScannerStatus(true);
            }
            updateLastUpdateTimestamp();
          }, 'image/jpeg', 0.7);
        } catch (err) {
          console.error('captureAndSend error', err);
          isRequesting = false;
        }
      }

      // esperar a que el video tenga metadatos para asegurar dimensiones
      video.addEventListener('loadedmetadata', function onMeta() {
        console.log('[scanner] video loadedmetadata', { w: video.videoWidth, h: video.videoHeight });
        // enviar primer frame ahora que sabemos las dimensiones
        try { captureAndSend(); } catch (e) { console.error('[scanner] capture error after metadata', e); }
        // iniciar intervalo regular
        intervalId = setInterval(captureAndSend, CAPTURE_INTERVAL);
        video.removeEventListener('loadedmetadata', onMeta);
      });

      // fallback: si no se dispara loadedmetadata en X ms, iniciar de todas formas
      setTimeout(() => {
        if (!intervalId) {
          console.warn('[scanner] loadedmetadata not fired, starting capture fallback');
          try { captureAndSend(); } catch (e) { console.error('[scanner] fallback capture error', e); }
          intervalId = setInterval(captureAndSend, CAPTURE_INTERVAL);
        }
      }, 1200);

    } catch (e) {
      console.error('camera start error', e);
      alert('No se pudo acceder a la cámara. Comprueba permisos.');
    }
  }

  function stop() {
    if (intervalId) clearInterval(intervalId);
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
    // ocultar vista previa de cámara, pero mantener resultados en DOM
    preview.style.display = 'none';
    startBtn.disabled = false;
    stopBtn.disabled = true;
    // marcar como "congelado" para que no se sobreescriban los resultados
    frozen = true;
    updateScannerStatus(false);
  }

  startBtn.addEventListener('click', start);
  stopBtn.addEventListener('click', stop);
}

function updateDetectionUI(data) {
  // data: {detected, detected_summary, mapped_ingredients, matching_recipes}
  const leftList = document.querySelector('.ingredients-list');
  if (leftList) {
    leftList.innerHTML = '';
    const detected = data.detected || [];
    detected.forEach(d => {
      const div = document.createElement('div');
      div.className = 'ingredient-item';
      div.innerHTML = `<i class="fas fa-check-circle"></i> <span>${d.label} ${d.score? '('+ (d.score*100).toFixed(0)+'%':''}</span>`;
      // mostrar frescura si existe
      if (d.freshness) {
        const fres = document.createElement('small');
        fres.style.display='block';
        fres.style.color = d.freshness === 'fresh' ? '#166534' : '#991b1b';
        fres.textContent = `Estado: ${d.freshness} ${d.freshness_conf? '('+ (d.freshness_conf*100).toFixed(0)+'%'+')':''}`;
        div.appendChild(fres);
      }
      leftList.appendChild(div);
    });
  }

  // rellenar recetas
  const recipesContainer = document.querySelector('.matching-recipes-card .recipes-list');
  if (recipesContainer) {
    recipesContainer.innerHTML = '';
    (data.matching_recipes || []).forEach(r => {
      const a = document.createElement('a');
      a.className = 'recipe-card';
      a.href = `/recipe/${r.id}/`;
      a.innerHTML = `
        <img src="${r.image_url||''}" alt="${r.nombre}" class="recipe-image" />
        <div class="recipe-info">
          <h4>${r.nombre}</h4>
          <div class="recipe-meta">
            <span class="recipe-match">${r.match_percentage}% coincidencia</span>
          </div>
        </div>
      `;
      recipesContainer.appendChild(a);
    });
  }
}

function updateScannerStatus(isLive) {
  const status = document.getElementById('scannerStatus');
  if (!status) return;
  if (isLive) {
    status.textContent = 'En vivo';
    status.classList.remove('badge-muted');
    status.classList.add('badge-success');
    status.style.background = '#10b981';
    status.style.color = '#fff';
  } else {
    status.textContent = 'Congelado';
    status.classList.remove('badge-success');
    status.classList.add('badge-muted');
    status.style.background = '#6b7280';
    status.style.color = '#fff';
  }
}

function updateLastUpdateTimestamp() {
  const el = document.getElementById('scannerLastUpdate');
  if (!el) return;
  const d = new Date();
  el.textContent = `Última actualización: ${d.toLocaleTimeString()}`;
}

// Auto-initialize camera UI if elements are present
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('startScannerBtn')) startCameraScan();
});
