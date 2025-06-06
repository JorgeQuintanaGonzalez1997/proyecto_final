document.addEventListener("DOMContentLoaded", function () {
    
    const sessionCookie = getCookie("cookieSesion");

    if (sessionCookie) {
        const idUsuario = sessionCookie.split('-')[1]; 
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
        console.log("ID de usuario:", idUsuario); 
        
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


        

    } else {
        console.log("No hay cookie de sesión. Redirigiendo al login...");
        window.location.href = "login.html"; 
    }
    
});


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
