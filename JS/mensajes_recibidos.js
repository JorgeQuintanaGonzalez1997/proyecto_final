document.addEventListener("DOMContentLoaded", function () {
    const mensajesContainer = document.getElementById("mensajesContainer");
    const modalMensaje = document.getElementById("modalMensaje");
    const cerrarModal = document.getElementById("cerrarModal");
    const respuestaTexto = document.getElementById("respuestaTexto");
    const btnEnviarRespuesta = document.getElementById("btnEnviarRespuesta");
    
    const sessionCookie = document.cookie.split("; ").find(row => row.startsWith("cookieSesion="));
    if (!sessionCookie) {
        mensajesContainer.innerHTML = "<p>No has iniciado sesión.</p>";
        return;
    }
    const idUsuario = sessionCookie.split("-")[1];



    
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

    
    fetch(`http://127.0.0.1:5000/mensaje/mensajes/${idUsuario}`, {
        method: "GET",
        credentials: "include"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(mensajes => {
        console.log("Mensajes cargados:", mensajes); 
        if (mensajes.error) {
            mensajesContainer.innerHTML = `<p>Error al cargar los mensajes: ${mensajes.error}</p>`;
            return;
        }
    
        
        if (mensajes.length === 0) {
            mensajesContainer.innerHTML = "<p>No tienes mensajes.</p>";
        } else {
            mensajes.forEach(mensaje => {
                const mensajeDiv = document.createElement("div");
                mensajeDiv.classList.add("mensaje");
                mensajeDiv.innerHTML = `
                    <p><strong>De:</strong> ${mensaje.remitente}</p>
                    <p><strong>Para:</strong> ${mensaje.destinatario}</p>
                    <p><strong>Mensaje:</strong> ${mensaje.mensaje}</p>
                    <p><strong>Fecha:</strong> ${new Date(mensaje.fecha).toLocaleString()}</p>
                    <button class="btnResponder" data-idUsuarioDestino="${mensaje.id_remitente}">Responder</button>
                    <hr>
                `;
                mensajesContainer.appendChild(mensajeDiv);
            });
    
           
            const botonesResponder = document.querySelectorAll(".btnResponder");
            
            botonesResponder.forEach(boton => {
                boton.addEventListener("click", function () {
                    const idUsuarioDestino = this.getAttribute("data-idUsuarioDestino");
                    abrirModalRespuesta(idUsuarioDestino);
                });
            });
        }
    })
    .catch(error => {
        console.error("Error al cargar los mensajes:", error);
        mensajesContainer.innerHTML = `<p>Error al cargar los mensajes: ${error.message}</p>`;
    });

    fetch(`http://127.0.0.1:5000/mensaje/marcar_leidos/${idUsuario}`, {
        method: "POST",
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.mensaje); 
    })
    .catch(error => console.error("Error al marcar mensajes como leídos:", error));


    
    function abrirModalRespuesta(idUsuarioDestino) {
        modalMensaje.style.display = "block";


        
        btnEnviarRespuesta.onclick = function () {
            const mensaje = respuestaTexto.value.trim();
            if (mensaje) {
                fetch("http://127.0.0.1:5000/mensaje/enviar", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    credentials: "include",
                    body: JSON.stringify({
                        idUsuarioRemitente: idUsuario, 
                        idUsuarioDestino: idUsuarioDestino, 
                        mensaje: mensaje
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.mensaje) {
                        alert("Respuesta enviada con éxito.");
                        modalMensaje.style.display = "none";
                    } else {
                        alert("Error al enviar la respuesta: " + data.error);
                    }
                })
                .catch(error => {
                    console.error("Error al enviar la respuesta:", error);
                });
            } else {
                alert("Escribe una respuesta antes de enviarla.");
            }
        };
    }
    
    cerrarModal.addEventListener("click", function () {
        modalMensaje.style.display = "none";
    });
});