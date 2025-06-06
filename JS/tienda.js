document.addEventListener("DOMContentLoaded", function () {
    
    const gridLibros = document.getElementById("gridLibros");
    const modalMensaje = document.getElementById("modalMensaje");
    const cerrarModal = document.getElementById("cerrarModal");
    const mensajeTexto = document.getElementById("mensajeTexto");
    const btnEnviarMensaje = document.getElementById("btnEnviarMensaje");
    const btnPujar=document.querySelectorAll('btnPujar');
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
    fetch("http://127.0.0.1:5000/libro/lista_libros", {
        method: "GET"
    })
    .then(response => response.json())
    .then(libros => {
        
        libros.forEach(libro => {
            const libroDiv = document.createElement("div");
            libroDiv.classList.add("grid-item");
            libroDiv.innerHTML = `
            <img src="data:image/jpeg;base64,${libro.imagen}" alt="${libro.titulo}" style="width: 100px; height: auto;">
                <h3>${libro.titulo}</h3>
                <p>Propietario ID: ${libro.idUsuario}</p>
                <p>Autor: ${libro.autor}</p>
                <p>Precio: ${libro.precio} €</p>

                <p>Monto Mayor: <span class="precio-actual" data-idLibro="${libro.id}"> </span></p>
                <p>Fecha límite para pujar: ${new Date(libro.fecha_limite).toLocaleString()}</p>
                
                <button class="btnPujar" data-idLibro="${libro.id}">Pujar</button>



                <button class="btnMensaje" data-idUsuario="${libro.idUsuario}" data-titulo="${libro.titulo}">Enviar mensaje</button>
            `;
            fetch(`http://127.0.0.1:5000/puja/mayor/${libro.id}`)
                .then(res => res.json())
                .then(data => {
                    const spanMonto = libroDiv.querySelector('.precio-actual');
                    if (data.monto !== null) {
                        spanMonto.textContent = `${data.monto} €      ID: ${data.idUsuario} Nombre: ${data.nombreUsuario}`;
                    } else {
                        spanMonto.textContent = "Sin pujas";
                    }
                });
            gridLibros.appendChild(libroDiv);
        });
        
        const botonesMensaje = document.querySelectorAll(".btnMensaje");
        botonesMensaje.forEach(boton => {
            boton.addEventListener("click", function () {
                idUsuarioDestino = this.getAttribute("data-idUsuario");
                const tituloLibro = this.getAttribute("data-titulo");
                abrirModal(tituloLibro);
            });
        });

        const botonesPujar = document.querySelectorAll('.btnPujar');
        botonesPujar.forEach(boton => {
            boton.addEventListener("click", function () {
                const idLibro = this.getAttribute("data-idLibro");
                const precioPuja = prompt("Introduce el precio de la puja:");
                console.log("ID del libro:", idLibro);
                hacerPuja(idLibro, precioPuja);
            });
        });

    })
    .catch(error => {
    console.error("Error al obtener los libros:", error);
    });
    
    
    
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
    
    function abrirModal(tituloLibro) {
        document.getElementById("infoLibro").innerText = `Mensaje sobre el libro: "${tituloLibro}"`;
        mensajeTexto.value = ""; 
        modalMensaje.style.display = "block";
    }
    function hacerPuja(idLibro, precioPuja) {
    if (precioPuja && !isNaN(precioPuja)) {
        fetch('http://127.0.0.1:5000/puja/pujarPrecio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ Libro: idLibro, Usuario: idUsuario, monto: precioPuja })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje || data.error);
            // Actualiza el monto mayor en la interfaz
            fetch(`http://127.0.0.1:5000/puja/mayor/${idLibro}`)
                .then(res => res.json())
                .then(data => {
                    const span = document.querySelector(`.precio-actual[data-idLibro="${idLibro}"]`);
                    if (data.monto !== null) {
                        span.textContent = `${data.monto} €      ID: ${data.idUsuario} Nombre: ${data.nombreUsuario}`;
                    } else {
                        span.textContent = "Sin pujas";
                    }
                });
        });
    } else {
        alert("Introduce un valor numérico válido para la puja.");
    }
    }
        

    
    cerrarModal.addEventListener("click", function () {
        modalMensaje.style.display = "none";
    });

    
    btnEnviarMensaje.addEventListener("click", function () {
        const mensaje = mensajeTexto.value.trim();
        if (mensaje) {
            console.log("ID del usuario destino:", idUsuarioDestino);
            fetch("http://127.0.0.1:5000/mensaje/enviar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials:"include",
                body: JSON.stringify({
                    idUsuarioDestino: idUsuarioDestino,
                    mensaje: mensaje
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje) {
                    alert("Mensaje enviado con éxito.");
                    modalMensaje.style.display = "none";
                } else {
                    alert("Error al enviar el mensaje: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error al enviar el mensaje:", error);
            });
        } else {
            alert("Por favor, escribe un mensaje antes de enviarlo.");
        }
    });
    
    
    
});
function hacerPuja(idLibro, precioPuja) {
    if (precioPuja && !isNaN(precioPuja)) {
        fetch('http://127.0.0.1:5000/puja/pujarPrecio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ Libro: idLibro, Usuario: idUsuario, monto: precioPuja })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje || data.error);
            // Actualiza el monto mayor en la interfaz
            fetch(`http://127.0.0.1:5000/puja/mayor/${idLibro}`)
                .then(res => res.json())
                .then(data => {
                    // Busca el span correspondiente y actualízalo
                    document.querySelector(`.precio-actual[data-idLibro="${idLibro}"]`).textContent =
                        data.monto !== null ? data.monto + " €" : "Sin pujas";
                });
        });
    } else {
        alert("Introduce un valor numérico válido para la puja.");
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

