// Saved Recipes JavaScript v1.0

document.addEventListener("DOMContentLoaded", function () {
  initializeFavoriteButtons();
  initializeViewButtons();
  addCardAnimations();
});

// Initialize favorite buttons
function initializeFavoriteButtons() {
  const favoriteButtons = document.querySelectorAll(".favorite-btn");

  favoriteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      toggleFavorite(this);
    });
  });
}

// Toggle favorite state
function toggleFavorite(button) {
  const recipeId = button.dataset.recipeId;
  const icon = button.querySelector("i");
  const isActive = button.classList.contains("active");

  // Animate the button
  button.style.transform = "scale(0.8)";
  setTimeout(() => {
    button.style.transform = "scale(1.2)";
    setTimeout(() => {
      button.style.transform = "scale(1)";
    }, 150);
  }, 150);

  if (isActive) {
    // Remove from favorites
    button.classList.remove("active");
    icon.className = "far fa-star";
    showNotification("Receta eliminada de favoritos", "info");

    // TODO: Make API call to remove from favorites
    // removeFavoriteAPI(recipeId);
  } else {
    // Add to favorites
    button.classList.add("active");
    icon.className = "fas fa-star";
    showNotification("Receta agregada a favoritos", "success");

    // TODO: Make API call to add to favorites
    // addFavoriteAPI(recipeId);
  }
}

// Initialize view buttons for history
function initializeViewButtons() {
  const viewButtons = document.querySelectorAll(".btn-view");

  viewButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const recipeId = this.dataset.recipeId;
      viewRecipeDetails(recipeId);
    });
  });
}

// View recipe details
function viewRecipeDetails(recipeId) {
  // Add loading animation
  const button = event.target;
  const originalText = button.textContent;
  button.textContent = "Cargando...";
  button.disabled = true;

  // Simulate loading
  setTimeout(() => {
    button.textContent = originalText;
    button.disabled = false;

    // TODO: Navigate to recipe detail page or open modal
    // window.location.href = `/recipes/${recipeId}/`;
    console.log(`Ver detalles de receta ID: ${recipeId}`);
    showNotification("Abriendo receta...", "info");
  }, 500);
}

// Add hover animations to cards
function addCardAnimations() {
  const cards = document.querySelectorAll(".favorite-card, .history-card");

  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transition = "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transition = "all 0.3s ease";
    });
  });
}

// Show notification (reuse from other modules)
function showNotification(message, type = "info") {
  // Check if notification system exists
  if (typeof window.showNotification === "function") {
    window.showNotification(message, type);
    return;
  }

  // Create simple notification
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${
          type === "success"
            ? "#4caf50"
            : type === "error"
            ? "#f44336"
            : "#2196f3"
        };
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Utility: Filter favorites by difficulty
function filterByDifficulty(difficulty) {
  const cards = document.querySelectorAll(".favorite-card");

  cards.forEach((card) => {
    const cardDifficulty = card
      .querySelector(".difficulty-badge")
      ?.textContent.trim();

    if (difficulty === "all" || cardDifficulty === difficulty) {
      card.style.display = "flex";
      card.style.animation = "fadeIn 0.3s ease";
    } else {
      card.style.display = "none";
    }
  });
}

// Utility: Sort history by date
function sortHistoryByDate(ascending = false) {
  const historyList = document.querySelector(".history-list");
  const cards = Array.from(historyList.querySelectorAll(".history-card"));

  cards.sort((a, b) => {
    const dateA = new Date(a.querySelector(".history-date").dataset.date);
    const dateB = new Date(b.querySelector(".history-date").dataset.date);
    return ascending ? dateA - dateB : dateB - dateA;
  });

  cards.forEach((card) => historyList.appendChild(card));
}

// Utility: Search in saved recipes
function searchRecipes(query) {
  query = query.toLowerCase().trim();

  if (!query) {
    // Show all cards
    document
      .querySelectorAll(".favorite-card, .history-card")
      .forEach((card) => {
        card.style.display = "";
      });
    return;
  }

  // Search in favorites
  document.querySelectorAll(".favorite-card").forEach((card) => {
    const title = card.querySelector("h3").textContent.toLowerCase();
    card.style.display = title.includes(query) ? "flex" : "none";
  });

  // Search in history
  document.querySelectorAll(".history-card").forEach((card) => {
    const title = card.querySelector("h3").textContent.toLowerCase();
    card.style.display = title.includes(query) ? "flex" : "none";
  });
}

// Export functions for external use
window.SavedRecipesModule = {
  filterByDifficulty,
  sortHistoryByDate,
  searchRecipes,
  toggleFavorite,
  viewRecipeDetails,
};
