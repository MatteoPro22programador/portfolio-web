// Abre los modales de edición y carga los datos si existen
document.querySelectorAll("[data-abrir]").forEach(function (boton) {
    boton.addEventListener("click", function () {
        var modal = document.getElementById(boton.dataset.abrir);
        var form = modal.querySelector("form");
        var item = boton.dataset.item ? JSON.parse(boton.dataset.item) : {};

        form.reset();
        form.querySelectorAll("[name]").forEach(function (campo) {
            if (campo.type === "file" || campo.name === "csrf_token") return;
            if (campo.name in item && item[campo.name] !== null) {
                campo.value = item[campo.name];
            }
        });

        var accion = item.id ? "Editar " : "Agregar ";
        modal.querySelector(".modal-titulo").textContent = accion + modal.dataset.nombre;
        modal.showModal();
    });
});

// Cierra los modales
document.querySelectorAll("dialog.modal").forEach(function (modal) {
    modal.querySelector("[data-cerrar]").addEventListener("click", function () {
        modal.close();
    });
    modal.addEventListener("click", function (e) {
        if (e.target === modal) modal.close();
    });
});

// Animaciones al mostrar secciones y habilidades
var CIRCUNFERENCIA = 2 * Math.PI * 52;

function llenarSkill(skill) {
    var nivel = Number(skill.dataset.nivel);
    var barra = skill.querySelector(".skill-barra");
    barra.style.strokeDashoffset = CIRCUNFERENCIA * (1 - nivel / 100);
}

var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("visible");
        entrada.target.querySelectorAll(".skill").forEach(llenarSkill);
        observador.unobserve(entrada.target);
    });
}, { threshold: 0.15 });

document.querySelectorAll(".reveal").forEach(function (seccion) {
    observador.observe(seccion);
});
