// file01.js
// Consume el API REST de landing_api conectado a Firebase Realtime Database

const API_URL = "/landing/api/index/";

// ============================
// 1. Cargar datos (Fetch GET)
// ============================
async function cargarDatos() {
  const container = document.getElementById("data-container");

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Error al obtener los datos");

    const data = await response.json();
    renderizarDatos(data, container);
  } catch (error) {
    container.innerHTML = `
      <div class="col-span-full text-center text-red-500 py-8 text-sm">
        No se pudieron cargar los datos: ${error.message}
      </div>`;
  }
}

function renderizarDatos(data, container) {
  if (!data || Object.keys(data).length === 0) {
    container.innerHTML = `
      <div class="col-span-full text-center text-muted py-8 text-sm">
        Aún no hay registros. Prueba enviando uno con el formulario.
      </div>`;
    return;
  }

  container.innerHTML = "";

  Object.entries(data).forEach(([id, item]) => {
    const card = document.createElement("div");
    card.className = "bg-white border border-line rounded-xl p-5 shadow-sm";
    card.innerHTML = `
      <div class="text-[11px] font-bold text-brand uppercase tracking-wider mb-1.5">${item.programa ?? "Registro"}</div>
      <div class="text-[15px] font-bold text-navy mb-1">${item.nombre ?? "Sin nombre"}</div>
      <div class="text-[13px] text-muted mb-2">${item.email ?? ""}</div>
      <div class="text-[11px] text-muted/70">${item.timestamp ?? ""}</div>
    `;
    container.appendChild(card);
  });
}

// ==================================
// 2. Enviar formulario (Fetch POST)
// ==================================
function mostrarAlerta(mensaje, tipo) {
  const alertBox = document.getElementById("form-alert");
  alertBox.textContent = mensaje;
  alertBox.className =
    "mb-4 p-3 rounded-md text-sm font-medium " +
    (tipo === "success"
      ? "bg-emerald-100 text-emerald-700"
      : "bg-red-100 text-red-700");
  alertBox.classList.remove("hidden");
}

function inicializarFormulario() {
  const form = document.getElementById("contact-form");
  const submitBtn = document.getElementById("submit-btn");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      programa: document.getElementById("programa").value,
      nombre: document.getElementById("nombre").value,
      email: document.getElementById("email").value,
    };

    submitBtn.disabled = true;
    submitBtn.textContent = "Enviando...";

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("El servidor rechazó la petición");

      await response.json();
      mostrarAlerta("Registro guardado correctamente.", "success");
      form.reset();
      cargarDatos(); // refresca la lista con el nuevo dato
    } catch (error) {
      mostrarAlerta("Error al enviar: " + error.message, "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Enviar Petición POST";
    }
  });
}

// ============================
// 3. Inicialización
// ============================
document.addEventListener("DOMContentLoaded", () => {
  cargarDatos();
  inicializarFormulario();
});