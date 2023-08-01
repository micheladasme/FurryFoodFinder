function showLoader() {
    var loaderContainer = document.getElementById("loader-container");
    loaderContainer.style.display = "flex";
}

function validarFormulario(event) {
    var nombreInput = document.getElementById("nombre_alimento");
    var nombreError = document.getElementById("error_nombre");

    if (nombreInput.value.trim() === "") {
    nombreError.style.display = "block";
    nombreInput.classList.add("is-danger");
    event.preventDefault();
    return false;
    } else {
    nombreError.style.display = "none";
    nombreInput.classList.remove("is-danger");
    return true;
    }
}