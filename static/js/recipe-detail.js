// Recipe Detail Functionality (limpio)
document.addEventListener("DOMContentLoaded", function () {
  // Función utilitaria para obtener la cookie CSRF
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  // Toggle favorito mediante llamada POST
  async function toggleFavorite(recipeId, button) {
    if (button) button.disabled = true;
    try {
      const res = await fetch(`/recipe/${recipeId}/favorite/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (res.status === 401) {
        window.location.href = `/auth/login/?next=${encodeURIComponent(window.location.pathname)}`;
        return;
      }

      if (!res.ok) {
        let errMsg = 'Error al guardar favorito';
        try {
          const errJson = await res.json();
          if (errJson && errJson.error) errMsg = errJson.error;
        } catch (e) {}
        throw new Error(errMsg);
      }

      let data = null;
      try {
        data = await res.json();
      } catch (e) {
        throw new Error('Respuesta inválida del servidor');
      }

      if (data.is_favorite) {
        button.classList.add('active');
        button.innerHTML = '<i class="fas fa-star"></i> Receta guardada';
      } else {
        button.classList.remove('active');
        button.innerHTML = '<i class="far fa-star"></i> Guardar receta';
      }
    } catch (e) {
      console.error(e);
      alert('No se pudo guardar la receta. Intenta de nuevo.');
    } finally {
      if (button) button.disabled = false;
    }
  }

  // Conectar el botón de guardar receta
  const saveButton = document.querySelector('.btn-save-recipe');
  if (saveButton) {
    saveButton.addEventListener('click', function () {
      const recipeId = this.getAttribute('data-recipe-id');
      toggleFavorite(recipeId, this);
    });
  }

  // Ingredient Click Toggle - TODOS los ingredientes son clickeables
  const ingredientItems = document.querySelectorAll(".ingredient-item");
  ingredientItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Toggle la clase available
      this.classList.toggle("available");

      // Actualizar el icono de check
      const checkIcon = this.querySelector(".check-icon");
      const itemIcon = this.querySelector(".item-icon");

      if (this.classList.contains("available")) {
        // Si está disponible, mostrar el check
        if (!checkIcon) {
          const newCheckIcon = document.createElement("i");
          newCheckIcon.className = "fas fa-check-circle check-icon";
          this.insertBefore(newCheckIcon, this.firstChild);
        }
        if (itemIcon) {
          itemIcon.style.marginLeft = "20px";
        }
      } else {
        // Si no está disponible, quitar el check
        if (checkIcon) {
          checkIcon.remove();
        }
        if (itemIcon) {
          itemIcon.style.marginLeft = "0";
        }
      }

      // Update availability counter
      updateAvailabilityCounter();
    });
  });

  // Update Availability Counter
  function updateAvailabilityCounter() {
    const totalIngredients = document.querySelectorAll(".ingredient-item").length;
    const availableIngredients = document.querySelectorAll(
      ".ingredient-item.available"
    ).length;
    const badge = document.querySelector(".availability-badge");

    if (badge) {
      badge.textContent = `${availableIngredients}/${totalIngredients} disponibles`;
    }
  }

  // Smooth Scroll Animation for Instructions
  const instructionSteps = document.querySelectorAll(".instruction-step");

  const observerOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -100px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateX(0)";
      }
    });
  }, observerOptions);

  instructionSteps.forEach((step) => {
    step.style.opacity = "0";
    step.style.transform = "translateX(-20px)";
    step.style.transition = "all 0.5s ease";
    observer.observe(step);
  });
});

// Nota: se eliminaron llamadas `await fetch` colocadas en top-level que rompían la ejecución.