function guardarContenido() {
    const contenidoTextarea = document.getElementById("contenido");
    const contenidoGrid = document.getElementById("contenidoGrid");
    const tituloSubForo = new URLSearchParams(window.location.search).get("titulo");
    const nuevoContenido = contenidoTextarea.value.trim();
    if (!nuevoContenido) {
        alert("Por favor, escribe algo antes de guardar.");
        return;
    }

    fetch(`http://127.0.0.1:5000/subForo/guardarContenido`, {
        method: "POST",
        credentials:"include",
        headers: {
            "Content-Type": "application/json"

        },
        body: JSON.stringify({
            titulo: tituloSubForo,
            contenido: nuevoContenido
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert("Contenido guardado con éxito.");
            const nuevoElemento = document.createElement("div");
            const nombreUsuario = document.getElementById("lblNombreUsuario").innerText;
            nuevoElemento.textContent = `${nombreUsuario}: ${nuevoContenido}`;
            nuevoElemento.style.marginBottom = "10px"; 
            contenidoGrid.appendChild(nuevoElemento);
            contenidoTextarea.value = ""; 
        }
    })
    .catch(error => console.error("Error al guardar el contenido:", error));
}
document.addEventListener("DOMContentLoaded", function () {
    const contenidoGrid = document.getElementById("contenidoGrid");
    const contenidoForm = document.getElementById("contenidoForm");
    const contenidoTextarea = document.getElementById("contenido");
    const tituloSubForo = new URLSearchParams(window.location.search).get("titulo");
    
    const sessionCookie = getCookie("cookieSesion");
    const idUsuario= sessionCookie.split("-")[1]
    
    if (sessionCookie) {
        
        console.log("Usuario autenticado. Cookie de sesión:", sessionCookie);
        
        fetch("http://127.0.0.1:5000/usuario/obtener_usuario", {
            method: "GET",
            credentials: "include" 
        })
        .then(response => response.json())
        .then(data => {
            if (data.nombre) {
                
                document.getElementById("lblNombreUsuario").innerText = data.nombre;
            } else {
                console.log("Error al obtener el nombre del usuario:", data.error);
                window.location.href = "login.html";
            }
        })
        .catch(error => {
            console.error("Error al obtener el nombre del usuario:", error);
            window.location.href = "login.html";
        });
    } else {
        console.log("No hay cookie de sesión. Redirigiendo al login...");
        window.location.href = "login.html";
    }
    fetch(`http://127.0.0.1:5000/mensaje/no_leidos/${idUsuario}`, {
            method: "GET",
            credentials: "include"
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensajes_no_leidos > 0) {
                console.log("Mensajes no leídos:", data.mensajes_no_leidos); 
                const notificacionMensajes = document.getElementById("notificacionMensajes");
                notificacionMensajes.style.display = "inline"; 
            }
            else {
                console.log("Mensajes no leídos:", data.mensajes_no_leidos);
                const notificacionMensajes = document.getElementById("notificacionMensajes");
                notificacionMensajes.style.display = "none"; 
            }
        })
        .catch(error => console.error("Error al verificar mensajes no leídos:", error));


    fetch(`http://127.0.0.1:5000/subForo/${tituloSubForo}`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const contenido = data.contenido.split("\n"); 
            contenido.forEach(linea => {
                if (linea.trim() !== "") { 
                    const nuevoElemento = document.createElement("div");
                    nuevoElemento.textContent = linea;
                    nuevoElemento.style.marginBottom = "10px";
                    contenidoGrid.appendChild(nuevoElemento);
                }
            });
        }
    })
    .catch(error => console.error("Error al cargar el contenido:", error));

   
    

    contenidoForm.addEventListener("submit", function (event) {
        event.preventDefault();
        guardarContenido();
    });
});
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}