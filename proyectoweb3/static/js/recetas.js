/**
 * Script para cargar recetas dinámicamente con Handlebars
 */

document.addEventListener('DOMContentLoaded', function () {

    // Compilar el template de Handlebars
    const templateSource = document.getElementById('receta-template').innerHTML;
    const template = Handlebars.compile(templateSource);

    // Contenedores
    const recetasContainer = document.getElementById('recetas-container');
    const loadingDiv = document.getElementById('loading');
    const sinRecetasDiv = document.getElementById('sin-recetas');
    const listaIngredientes = document.getElementById('lista-ingredientes');

    // Función para cargar recetas desde la API
    async function cargarRecetas() {
        try {
            // Mostrar loading
            loadingDiv.style.display = 'block';
            recetasContainer.style.display = 'none';
            sinRecetasDiv.style.display = 'none';

            // Hacer petición a la API
            const response = await fetch('/api/recetas-generadas/');
            const data = await response.json();

            // Mostrar ingredientes
            if (data.ingredientes && data.ingredientes.length > 0) {
                listaIngredientes.textContent = data.ingredientes.join(', ');
            } else {
                listaIngredientes.textContent = 'No hay ingredientes seleccionados';
            }

            // Ocultar loading
            loadingDiv.style.display = 'none';

            // Si hay recetas, renderizarlas
            if (data.recetas && data.recetas.length > 0) {
                const html = template(data);
                recetasContainer.innerHTML = html;
                recetasContainer.style.display = 'flex';
            } else {
                // Mostrar mensaje de no hay recetas
                sinRecetasDiv.style.display = 'block';
            }

        } catch (error) {
            console.error('Error al cargar recetas:', error);
            loadingDiv.style.display = 'none';
            sinRecetasDiv.style.display = 'block';
            sinRecetasDiv.innerHTML = '<p class="text-center text-danger">Error al cargar las recetas. Intenta de nuevo.</p>';
        }
    }

    // Cargar recetas al iniciar la página
    cargarRecetas();

    // Opcional: botón para recargar recetas
    const btnRecargar = document.getElementById('btn-recargar-recetas');
    if (btnRecargar) {
        btnRecargar.addEventListener('click', cargarRecetas);
    }
});