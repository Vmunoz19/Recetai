/**
 * Sistema de notificaciones auto-dismissible
 * Cierra automáticamente las alertas después de 5 segundos
 */

document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert-dismissible");

  alerts.forEach(function (alert) {
    // Auto-cerrar después de 5 segundos
    setTimeout(function () {
      alert.style.animation = "fadeOut 0.3s ease-in";

      // Remover del DOM después de la animación
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 5000);
  });

  // Manejar el botón de cerrar manualmente
  const closeButtons = document.querySelectorAll(".alert-close");
  closeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const alert = this.parentElement;
      alert.style.animation = "fadeOut 0.3s ease-in";
      setTimeout(function () {
        alert.remove();
      }, 300);
    });
  });
});
