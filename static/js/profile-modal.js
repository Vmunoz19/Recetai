// Profile Modal JavaScript v1.0

document.addEventListener("DOMContentLoaded", function () {
  initializeProfileModal();
});

// Initialize profile modal
function initializeProfileModal() {
  const modal = document.getElementById("profileModal");
  const closeBtn = document.querySelector(".profile-modal-close");
  const overlay = document.querySelector(".profile-modal-overlay");
  const btnEditProfile = document.getElementById("btnEditProfile");
  const btnCloseProfile = document.getElementById("btnCloseProfile");
  const btnCancelEdit = document.getElementById("btnCancelEdit");
  const profileForm = document.getElementById("profileEditForm");
  const photoInput = document.getElementById("profilePhotoInput");

  // Triggers para abrir el modal (agregados desde el sidebar o menú)
  const profileTriggers = document.querySelectorAll("[data-profile-trigger]");

  if (!modal) return;

  // Abrir modal
  profileTriggers.forEach((trigger) => {
    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      openProfileModal();
    });
  });

  // Cerrar modal
  if (closeBtn) {
    closeBtn.addEventListener("click", closeProfileModal);
  }

  if (overlay) {
    overlay.addEventListener("click", closeProfileModal);
  }

  if (btnCloseProfile) {
    btnCloseProfile.addEventListener("click", closeProfileModal);
  }

  // Cambiar a modo edición
  if (btnEditProfile) {
    btnEditProfile.addEventListener("click", function () {
      showEditMode();
    });
  }

  // Cancelar edición
  if (btnCancelEdit) {
    btnCancelEdit.addEventListener("click", function () {
      showViewMode();
    });
  }

  // Enviar formulario
  if (profileForm) {
    profileForm.addEventListener("submit", function (e) {
      e.preventDefault();
      saveProfile();
    });
  }

  // Preview de foto
  if (photoInput) {
    photoInput.addEventListener("change", function (e) {
      previewPhoto(e);
    });
  }

  // Cerrar con tecla ESC
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      closeProfileModal();
    }
  });
}

// Abrir modal
function openProfileModal() {
  const modal = document.getElementById("profileModal");
  if (modal) {
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
    showViewMode();
  }
}

// Cerrar modal
function closeProfileModal() {
  const modal = document.getElementById("profileModal");
  if (modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "";
    showViewMode();
  }
}

// Mostrar modo vista
function showViewMode() {
  const viewMode = document.getElementById("profileViewMode");
  const editMode = document.getElementById("profileEditMode");

  if (viewMode) viewMode.style.display = "block";
  if (editMode) editMode.style.display = "none";
}

// Mostrar modo edición
function showEditMode() {
  const viewMode = document.getElementById("profileViewMode");
  const editMode = document.getElementById("profileEditMode");

  if (viewMode) viewMode.style.display = "none";
  if (editMode) editMode.style.display = "block";
}

// Guardar perfil
async function saveProfile() {
  const form = document.getElementById("profileEditForm");
  const saveBtn = document.getElementById("btnSaveProfile");
  const formData = new FormData(form);

  // Debug: Ver qué datos se están enviando
  console.log("Enviando datos del perfil:");
  for (let pair of formData.entries()) {
    console.log(pair[0] + ": " + pair[1]);
  }

  // Deshabilitar botón y mostrar loading
  saveBtn.disabled = true;
  saveBtn.classList.add("loading");

  try {
    const response = await fetch("/auth/profile/", {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const data = await response.json();

    console.log("Respuesta del servidor:", data);
    console.log("Status de respuesta:", data.status);
    console.log("Response.ok:", response.ok);

    if (response.ok && data.status === "success") {
      console.log("Guardado exitoso, actualizando display...");

      // Actualizar información en la vista
      updateProfileDisplay(data.user);

      // Mostrar notificación de éxito
      showProfileNotification("Perfil actualizado correctamente", "success");

      // Volver al modo vista inmediatamente
      console.log("Cambiando a modo vista...");
      showViewMode();
    } else {
      console.log("Error en la respuesta:", data);
      // Mostrar errores
      console.error("Errores:", data.errors);
      if (data.errors) {
        displayFormErrors(data.errors);
      }
      showProfileNotification(
        data.message || "Error al actualizar el perfil",
        "error"
      );
    }
  } catch (error) {
    console.error("Error de conexión:", error);
    showProfileNotification("Error de conexión. Intenta nuevamente.", "error");
  } finally {
    // Habilitar botón y quitar loading
    saveBtn.disabled = false;
    saveBtn.classList.remove("loading");
  }
}

// Actualizar información en la vista
function updateProfileDisplay(user) {
  const displayName = document.getElementById("displayName");
  const displayEmail = document.getElementById("displayEmail");
  const displayPhone = document.getElementById("displayPhone");
  const displayNationalId = document.getElementById("displayNationalId");
  const displayAddress = document.getElementById("displayAddress");
  const displayCity = document.getElementById("displayCity");
  const displayGender = document.getElementById("displayGender");

  if (displayName && user.first_name && user.last_name) {
    displayName.textContent = `${user.first_name} ${user.last_name}`;
  }

  if (displayEmail && user.email) {
    displayEmail.textContent = user.email;
  }

  if (displayPhone) {
    const phoneGroup = displayPhone.closest(".info-group");
    if (user.phone_number) {
      displayPhone.textContent = user.phone_number;
      if (phoneGroup) phoneGroup.style.display = "flex";
    } else {
      if (phoneGroup) phoneGroup.style.display = "none";
    }
  }

  if (displayNationalId) {
    const idGroup = displayNationalId.closest(".info-group");
    if (user.national_id) {
      displayNationalId.textContent = user.national_id;
      if (idGroup) idGroup.style.display = "flex";
    } else {
      if (idGroup) idGroup.style.display = "none";
    }
  }

  if (displayAddress) {
    const addressGroup = displayAddress.closest(".info-group");
    if (user.address) {
      displayAddress.textContent = user.address;
      if (addressGroup) addressGroup.style.display = "flex";
    } else {
      if (addressGroup) addressGroup.style.display = "none";
    }
  }

  if (displayCity) {
    const cityGroup = displayCity.closest(".info-group");
    if (user.city) {
      displayCity.textContent = user.city;
      if (cityGroup) cityGroup.style.display = "flex";
    } else {
      if (cityGroup) cityGroup.style.display = "none";
    }
  }

  if (displayGender) {
    const genderGroup = displayGender.closest(".info-group");
    if (user.gender) {
      let genderText = user.gender;
      if (user.gender === "M") genderText = "Masculino";
      else if (user.gender === "F") genderText = "Femenino";

      displayGender.textContent = genderText;
      if (genderGroup) genderGroup.style.display = "flex";
    } else {
      if (genderGroup) genderGroup.style.display = "none";
    }
  }

  // Actualizar avatar si hay foto
  if (user.profile_photo) {
    updateAvatarImage(user.profile_photo);
  }
}

// Preview de foto antes de guardar
function previewPhoto(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Validar que sea imagen
  if (!file.type.startsWith("image/")) {
    showNotification("Por favor selecciona una imagen válida", "error");
    event.target.value = "";
    return;
  }

  // Validar tamaño (máx 5MB)
  if (file.size > 5 * 1024 * 1024) {
    showNotification("La imagen no debe superar 5MB", "error");
    event.target.value = "";
    return;
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    const avatarPreview = document.getElementById("avatarPreview");
    const avatarIcon = document.getElementById("avatarIcon");
    const currentAvatar = document.getElementById("currentAvatar");

    // Remover icono si existe
    if (avatarIcon) {
      avatarIcon.remove();
    }

    // Actualizar o crear imagen
    if (currentAvatar) {
      currentAvatar.src = e.target.result;
    } else {
      const img = document.createElement("img");
      img.src = e.target.result;
      img.alt = "Vista previa";
      img.className = "avatar-image";
      img.id = "currentAvatar";
      avatarPreview.appendChild(img);
    }
  };
  reader.readAsDataURL(file);
}

// Actualizar imagen de avatar en ambos modos
function updateAvatarImage(photoUrl) {
  // Actualizar en modo vista
  const viewAvatar = document.querySelector("#profileViewMode .avatar-circle");
  if (viewAvatar) {
    viewAvatar.innerHTML = `<img src="${photoUrl}" alt="Foto de perfil" class="avatar-image">`;
  }

  // Actualizar en modo edición
  const editAvatar = document.querySelector("#profileEditMode .avatar-circle");
  if (editAvatar) {
    editAvatar.innerHTML = `<img src="${photoUrl}" alt="Foto de perfil" class="avatar-image" id="currentAvatar">`;
  }

  // Actualizar en sidebar
  const sidebarProfileBtn = document.querySelector(".nav-item-profile");
  if (sidebarProfileBtn) {
    sidebarProfileBtn.innerHTML = `<img src="${photoUrl}" alt="Perfil" class="profile-photo-icon">`;
  }
}

// Mostrar errores del formulario
function displayFormErrors(errors) {
  // Limpiar errores previos
  document.querySelectorAll(".form-group").forEach((group) => {
    group.classList.remove("error");
    const errorMsg = group.querySelector(".form-error");
    if (errorMsg) errorMsg.remove();
  });

  // Mostrar nuevos errores
  for (const [field, messages] of Object.entries(errors)) {
    const input = document.querySelector(`[name="${field}"]`);
    if (input) {
      const formGroup = input.closest(".form-group");
      if (formGroup) {
        formGroup.classList.add("error");
        const errorDiv = document.createElement("div");
        errorDiv.className = "form-error";
        errorDiv.textContent = messages[0];
        formGroup.appendChild(errorDiv);
        // Eliminar el mensaje de error después de 10 segundos
        setTimeout(() => {
          if (errorDiv && errorDiv.parentNode) {
            errorDiv.parentNode.classList.remove("error");
            errorDiv.remove();
          }
        }, 10000);
      }
    }
  }
}

// Mostrar notificación
function showProfileNotification(message, type = "info") {
  // Verificar si existe el sistema global de notificaciones
  if (typeof window.showNotification === "function") {
    window.showNotification(message, type);
    return;
  }

  // Crear notificación simple
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
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10001;
        animation: slideIn 0.3s ease;
        font-family: var(--font-family);
        font-size: 14px;
        font-weight: 500;
        max-width: 350px;
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease";
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Función para obtener cookie CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Exportar funciones
window.ProfileModal = {
  open: openProfileModal,
  close: closeProfileModal,
  showEditMode,
  showViewMode,
};
