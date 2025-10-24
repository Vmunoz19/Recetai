/**
 * Funcionalidad del Sidebar
 * Maneja las interacciones del menú lateral
 */

document.addEventListener("DOMContentLoaded", function () {
  // Manejar clics en elementos "Próximamente"
  const comingSoonLinks = document.querySelectorAll('a[title*="Próximamente"]');

  comingSoonLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      alert("Funcionalidad en desarrollo");
    });
  });
});
