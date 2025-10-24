// Recipe Detail Functionality
document.addEventListener("DOMContentLoaded", function () {
  // Save Recipe Button
  const saveButton = document.querySelector(".btn-save-recipe");
  if (saveButton) {
    saveButton.addEventListener("click", function () {
      // Toggle saved state
      const icon = this.querySelector("i");
      if (icon.classList.contains("far")) {
        icon.classList.remove("far");
        icon.classList.add("fas");
        this.textContent = " Receta guardada";
        this.prepend(icon);
        // Aquí puedes agregar lógica para guardar en el backend
      } else {
        icon.classList.remove("fas");
        icon.classList.add("far");
        this.textContent = " Guardar receta";
        this.prepend(icon);
      }
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
    const totalIngredients =
      document.querySelectorAll(".ingredient-item").length;
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
