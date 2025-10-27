// static/js/recipes.js

// DEBUG: indicar que el script cargó
console.log('[recipe.js] loaded');

// Guard global para evitar inicializar el mismo script dos veces
if (window.__recipe_js_inited) {
  console.log('[recipe.js] already initialized, skipping duplicate init');
} else {
  window.__recipe_js_inited = true;


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

async function toggleFavorite(recipeId, button) {
  // prevenir dobles envíos
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
  console.log('[favorite] fetch status', res.status);
  if (res.status === 401) {
      // No autenticado: redirigir a login (útil en peticiones AJAX)
      window.location.href = `/auth/login/?next=${encodeURIComponent(window.location.pathname)}`;
      return;
    }

    if (!res.ok) {
      // intentar leer JSON con mensaje de error
      let errMsg = 'Error al guardar favorito';
      try {
        const errJson = await res.json();
        if (errJson && errJson.error) errMsg = errJson.error;
      } catch (e) {
        // no JSON
      }
      throw new Error(errMsg);
    }

    let data = null;
    try {
      data = await res.json();
      console.log('[favorite] response json', data);
    } catch (e) {
      throw new Error('Respuesta inválida del servidor');
    }

    const icon = button.querySelector('i');
    if (data.is_favorite) {
      button.classList.add('active');
      icon.classList.remove('far');
      icon.classList.add('fas');
    } else {
      button.classList.remove('active');
      icon.classList.remove('fas');
      icon.classList.add('far');
    }
    } catch (e) {
    console.error(e);
    alert('No se pudo guardar la receta. Intenta de nuevo.');
    } finally {
      if (button) button.disabled = false;
    }
}

function initFavoriteButtons() {
  document.querySelectorAll('.btn-favorite').forEach(btn => {
    // evitar dobles listeners
    if (btn.dataset._favInit === '1') return;
    btn.dataset._favInit = '1';
    btn.addEventListener('click', (ev) => {
      ev.preventDefault();
      const recipeId = btn.getAttribute('data-recipe-id');
      toggleFavorite(recipeId, btn);
    });
  });
}

function initFilterPanel() {
  console.log('[recipe.js] initFilterPanel start');
  const panel = document.querySelector('.filters-panel');
  const toggleBtn = document.querySelector('.filters-toggle-btn');
  console.log('[recipe.js] toggleBtn, panel:', toggleBtn, panel);

  // If panel is inline (always visible) we don't need the toggle button or positioning logic.
  if (panel && panel.classList.contains('inline')) {
    console.log('[recipe.js] panel is inline — skipping interactive init');
    try { panel.inert = false; } catch (e) { /* ignore */ }
    panel.setAttribute('aria-hidden', 'false');
    panel.classList.add('open');
    // initialize favorites only and skip interactive toggle setup
    return;
  }

  if (!toggleBtn || !panel) {
    console.log('[recipe.js] initFilterPanel: elements not found');
    return;
  }
  // evitar doble inicialización del panel si el script corre dos veces
  if (toggleBtn.dataset._filterInit === '1') {
    console.log('[recipe.js] filter panel already initialized on this element');
    return;
  }
  toggleBtn.dataset._filterInit = '1';
  // helper: focusable selectors
  const focusableSelector = 'a, button, input, select, textarea, [tabindex]';

  function setPanelHidden(hidden) {
    console.log('[recipe.js] setPanelHidden ->', hidden);
    if (hidden) {
      panel.setAttribute('aria-hidden', 'true');
      panel.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
      // make inert if supported
      try { panel.inert = true; } catch (e) { /* ignore */ }
      // remove focusability
      panel.querySelectorAll(focusableSelector).forEach(el => {
        // store previous tabindex
        if (el.hasAttribute('tabindex')) el.dataset._prevTab = el.getAttribute('tabindex');
        el.setAttribute('tabindex', '-1');
      });
      // clear inline positioning so it doesn't persist when hidden
      try {
        panel.style.left = '';
        panel.style.top = '';
        // keep position fixed default from CSS; no need to modify
      } catch (e) { /* ignore */ }
    } else {
      panel.setAttribute('aria-hidden', 'false');
      panel.classList.add('open');
      toggleBtn.setAttribute('aria-expanded', 'true');
      try { panel.inert = false; } catch (e) { /* ignore */ }
      // restore tabindex
      panel.querySelectorAll(focusableSelector).forEach(el => {
        if (el.dataset._prevTab !== undefined) {
          el.setAttribute('tabindex', el.dataset._prevTab);
          delete el.dataset._prevTab;
        } else {
          el.removeAttribute('tabindex');
        }
      });
      // focus first focusable element
      const first = panel.querySelector('input, select, button, a');
      if (first) first.focus();

      // Position the panel next to the toggle button on wide screens.
      try {
        if (window.innerWidth > 768) {
          // ensure panel uses fixed positioning (CSS default)
          panel.style.position = 'fixed';
          const btnRect = toggleBtn.getBoundingClientRect();
          // if panel has no width yet (hidden), temporarily make it visible to measure
          const prevOpacity = panel.style.opacity;
          const prevPointer = panel.style.pointerEvents;
          panel.style.opacity = '0';
          panel.style.pointerEvents = 'none';
          panel.classList.add('open');
          const panelW = panel.offsetWidth || 520;
          // compute left to place panel to the right of the button
          let left = Math.round(btnRect.right + 8);
          // if it would overflow to the right, place to the left of the button
          if (left + panelW > window.innerWidth - 8) {
            left = Math.round(btnRect.left - panelW - 8);
            panel.style.transformOrigin = 'right top';
          } else {
            panel.style.transformOrigin = 'left top';
          }
          // vertical align top to button top (can be adjusted)
          const top = Math.round(btnRect.top);
          panel.style.left = `${left}px`;
          panel.style.top = `${top}px`;
          // restore previous inline styles for opacity/pointer (visibility controlled with classes)
          panel.style.opacity = prevOpacity;
          panel.style.pointerEvents = prevPointer;
        } else {
          // on small screens we want the panel to be static/full-width (CSS media query handles it)
          panel.style.position = '';
          panel.style.left = '';
          panel.style.top = '';
        }
      } catch (e) {
        console.warn('[recipe.js] error positioning panel', e);
      }
    }
    // Log computed styles and bounding rect for debugging visual issues
    try {
      const rect = panel.getBoundingClientRect();
      const cs = window.getComputedStyle(panel);
      console.log('[recipe.js] panel rect', rect);
      console.log('[recipe.js] panel computed style opacity', cs.getPropertyValue('opacity'));
      console.log('[recipe.js] panel computed transform', cs.getPropertyValue('transform'));
      console.log('[recipe.js] panel aria-hidden', panel.getAttribute('aria-hidden'));
      console.log('[recipe.js] panel classList', panel.classList.toString());
    } catch (e) {
      console.warn('[recipe.js] error reading panel rect/style', e);
    }
  }

  // If any descendant already has focus when the page loads, move focus away to avoid aria-hidden conflict
  if (panel.contains(document.activeElement)) {
    // move focus to the toggle button
    try { toggleBtn.focus(); } catch (e) { /* ignore */ }
    setPanelHidden(true);
  } else {
    // ensure panel starts hidden and inert
    setPanelHidden(true);
  }

  function openPanel() { console.log('[recipe.js] openPanel'); setPanelHidden(false); }
  function closePanel() { console.log('[recipe.js] closePanel'); setPanelHidden(true); }

  toggleBtn.addEventListener('click', (e) => {
    console.log('[recipe.js] filters-toggle clicked (handler)');
    const isOpen = panel.classList.contains('open');
    console.log('[recipe.js] panel isOpen before click:', isOpen);
    if (isOpen) closePanel(); else openPanel();
    console.log('[recipe.js] panel isOpen after click:', panel.classList.contains('open'));
  });

  // cerrar al click fuera
  document.addEventListener('click', (e) => {
    if (!panel.classList.contains('open')) return;
    if (e.target === toggleBtn) return;
    if (!panel.contains(e.target) && !toggleBtn.contains(e.target)) {
      closePanel();
    }
  });

  // cerrar con Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && panel.classList.contains('open')) {
      closePanel();
      toggleBtn.focus();
    }
  });
}
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFilterPanel);
  } else {
    initFilterPanel();
  }

  // Si el script se carga después de DOMContentLoaded, el listener no se disparará.
  // Por eso intentamos inicializar de forma inmediata y también en DOMContentLoaded.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFavoriteButtons);
  } else {
    initFavoriteButtons();
  }

} // fin guard global __recipe_js_inited
// Nota: se quitó código erróneo que hacía un `await fetch` en top-level
// y que provocaba errores de ejecución en el navegador.