





document.getElementById("formCrearSubForo").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let titulo = document.getElementById("nombreSubForo").value;

    fetch('http://127.0.0.1:5000/subForo/crear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ titulo: titulo })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            cargarSubForos(); 
            document.getElementById("nombreSubForo").value = "";
        }
    })
    .catch(error => console.error('Error:', error));
});
document.addEventListener("DOMContentLoaded", function () {
    cargarSubForos();
    
    const sessionCookie = getCookie("cookieSesion");
    const idUsuario= sessionCookie.split("-")[1]
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

    if (sessionCookie) {
        console.log("Usuario identificado:", sessionCookie);
        
        fetch("http://127.0.0.1:5000/usuario/obtener_usuario", {
            method: "GET",
            credentials: "include" 
        })
        .then(response => response.json())
        .then(data => {
            if (data.nombre) {
                
                document.getElementById("lblNombreUsuario").innerText = data.nombre;
            } else {
                console.log("Error del usuario:", data.error);
                window.location.href = "login.html"; 
            }
        })
        .catch(error => {
            console.error("Error del usuario:", error);
            window.location.href = "login.html"; 
        });
        
    } else {
        console.log("No hay cookie.");
        window.location.href = "login.html"; 
    }
    
});


function getCookie(name) {
    const valor = `; ${document.cookie}`;
    const partes = valor.split(`; ${name}=`);
    if (partes.length === 2) return partes.pop().split(';').shift();
}
function cargarSubForos() {
    fetch('http://127.0.0.1:5000/subForo/listar')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const listaEnlaces = document.getElementById("listaEnlaces");
                listaEnlaces.innerHTML = ""; 
                data.subForos.forEach(subForo => {
                    let nuevoElemento = document.createElement("li");
                    let enlace = document.createElement("a");
                    enlace.href = `sub_foro.html?titulo=${encodeURIComponent(subForo.titulo)}`;
                    enlace.textContent = subForo.titulo;
                    nuevoElemento.appendChild(enlace);
                    listaEnlaces.appendChild(nuevoElemento);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}
