const form = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const listarBtn = document.getElementById("listarBtn");

let mostrando = false; // estado inicial: oculto

listarBtn.addEventListener("click", async () => {
  if (mostrando) {
    // Si ya se están mostrando, las ocultamos
    taskList.innerHTML = "";
    mostrando = false;
    listarBtn.textContent = "📋 Listar tareas"; // vuelve al texto original
  } else {
    // Si están ocultas, las cargamos
    await cargarTareas();
    mostrando = true;
    listarBtn.textContent = "❌ Ocultar tareas"; // cambia el texto del botón
  }
});

async function cargarTareas() {
  try {
    const res = await fetch("http://127.0.0.1:5000/tareas");
    const tareas = await res.json();

    taskList.innerHTML = ""; // limpia la lista

    if (tareas.length === 0) {
      taskList.innerHTML = "<li>No hay tareas registradas</li>";
      return;
    }
    
    tareas.forEach(t => {
      const li = document.createElement("li");
      li.innerHTML = `
        ${t.titulo} - ${t.descripcion} [${t.estado}]
        <button class="task-btn edit-btn">✏ Editar</button>
        <button class="task-btn delete-btn">❌ Eliminar</button>
        <button class="task-btn complete-btn">✅ Completada</button>
      `;

      // Si la tarea ya está completada, aplica estilo
      if (t.estado === "completada") {
        li.classList.add("completed");
      }

      // Botón eliminar
      li.querySelector(".delete-btn").addEventListener("click", async () => {
        try {
          const res = await fetch(`http://127.0.0.1:5000/tareas/${t.id}`, {
            method: "DELETE"
          });
          if (res.ok) {
            cargarTareas(); // refresca lista
          }
        } catch (err) {
          console.error("Error al eliminar tarea:", err);
        }
      });

      // Botón editar
      li.querySelector(".edit-btn").addEventListener("click", async () => {
        const nuevoTitulo = prompt("Nuevo título:", t.titulo);
        const nuevaDescripcion = prompt("Nueva descripción:", t.descripcion);

        if (nuevoTitulo !== null && nuevoTitulo.trim() !== "") {
          try {
            const res = await fetch(`http://127.0.0.1:5000/tareas/${t.id}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                titulo: nuevoTitulo,
                descripcion: nuevaDescripcion,
                estado: t.estado   // 👈 mantenemos el estado actual
              })
            });
            if (res.ok) {
              cargarTareas(); // refresca lista
            }
          } catch (err) {
            console.error("Error al editar tarea:", err);
          }
        }
      });

      // Botón completar (cambia estado)
      li.querySelector(".complete-btn").addEventListener("click", async () => {
        const nuevoEstado = t.estado === "pendiente" ? "completada" : "pendiente"; // alterna
        try {
          const res = await fetch(`http://127.0.0.1:5000/tareas/${t.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              titulo: t.titulo,
              descripcion: t.descripcion,
              estado: nuevoEstado   // 👈 enviamos el nuevo estado
            })
          });
          if (res.ok) {
            cargarTareas(); // refresca lista
          }
        } catch (err) {
          console.error("Error al cambiar estado:", err);
        }
      });

      taskList.appendChild(li);
    });
  } catch (err) {
    console.error("Error al cargar tareas:", err);
  }
}

// Evento para crear tarea (POST al backend)
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const titulo = document.getElementById("titulo").value;
  const descripcion = document.getElementById("descripcion").value;

  try {
    const res = await fetch("http://127.0.0.1:5000/tareas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo, descripcion, estado: "pendiente" }) // 👈 estado inicial
    });

    const data = await res.json();
    console.log("Respuesta del backend:", data);

    form.reset();   // limpia el formulario
  } catch (err) {
    console.error("Error al crear tarea:", err);
  }
});
