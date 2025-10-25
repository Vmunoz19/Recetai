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
