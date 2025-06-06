document.addEventListener("DOMContentLoaded", function () {
    
    const sessionCookie = getCookie("cookieSesion");
    const gridVentas = document.getElementById("gridVentas");
    const modalMensaje = document.getElementById("modalMensaje");
    const btnAgregarLibro = document.getElementById("btnAgregarLibro");
    const formAgregarLibro = document.getElementById("formAgregarLibro");
    const btnGuardarLibro = document.getElementById("btnGuardarLibro");
    const btnCancelar = document.getElementById("btnCancelar");

    if (sessionCookie) {
        const idUsuario = sessionCookie.split('-')[1]; 
        fetch(`http://127.0.0.1:5000/libro/lista_libros_por_usuario/${idUsuario}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(libros => {
            
            libros.forEach(libro => {
                const libroDiv = document.createElement("div");
                libroDiv.classList.add("grid-item");
                libroDiv.innerHTML = `
                    <h3>${libro.titulo}</h3>
                    <img src="data:image/jpeg;base64,${libro.imagen}" alt="${libro.titulo}" style="width: 100px; height: auto;">
                    <p>Autor: ${libro.autor}</p>
                    <p>Precio: ${libro.precio} €</p>
                    <p>Fecha límite para pujar: ${new Date(libro.fecha_limite).toLocaleString()}</p>
                    <button class="btnEliminar" data-idLibro="${libro.id}">Eliminar</button>
                `;
                gridVentas.appendChild(libroDiv);
            });
        
            
            
        const botonesEliminar = document.querySelectorAll(".btnEliminar");
        botonesEliminar.forEach(boton => {
            boton.addEventListener("click", function () {
                idLibro = this.getAttribute("data-idLibro");
                console.log("ID del libro a eliminar:", idLibro); 
                eliminarLibro(idLibro);
            });
        });
        })
        .catch(error => {
            console.error("Error al obtener los libros:", error);
        });
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

        
        function eliminarLibro(idLibro) {
            if (confirm("¿Estás seguro de que deseas eliminar este libro?")) {
                fetch(`http://127.0.0.1:5000/libro/eliminar/${idLibro}`, {
                    method: "DELETE",
                    credentials: "include"
                })
                .then(response => response.json())
                .then(data => {
                    if (data.mensaje) {
                        alert("Libro eliminado con éxito.");
                        location.reload(); 
                    } else {
                        alert("Error al eliminar el libro: " + data.error);
                    }
                })
                .catch(error => {
                    console.error("Error al eliminar el libro:", error);
                });
            }
        }

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
        formAgregarLibro.addEventListener("submit", function (event) {
            event.preventDefault(); 

            const formData = new FormData(this); 
            formData.append("idUsuario", idUsuario); 

            fetch("http://127.0.0.1:5000/libro/registrar", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Infor: ",data);
                if (data.mensaje) {
                    alert("Libro registrado con éxito.");
                    formAgregarLibro.style.display = "none";
                    location.reload(); 
                } else {
                    alert("Error al registrar el libro: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error al registrar el libro:", error);
            });
        });
        // btnGuardarLibro.addEventListener("click", function () {
    
        //     const titulo = document.getElementById("titulo").value;
        //     const autor = document.getElementById("autor").value;
        //     const tipo = document.getElementById("tipo").value;
        //     const precio = document.getElementById("precio").value;
            
        
        //     fetch(`http://127.0.0.1:5000/libro/registrar`, {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/json"
        //         },
        //         body: JSON.stringify({
        //             titulo: titulo,
        //             autor: autor,
        //             tipo: tipo,
        //             precio: parseFloat(precio),
        //             idUsuario: idUsuario,
                    
                    
        //         })
        //     })
        //     .then(response => response.json())
        //     .then(data => {
        //         if (data.mensaje) {
        //             alert("Libro añadido con éxito");
        //             formAgregarLibro.style.display = "none";
        //             location.reload(); // Recargar la página para mostrar el nuevo libro
        //         } else {
        //             alert("Error al añadir el libro: " + data.error);
        //         }
        //     })
        //     .catch(error => {
        //         console.error("Error al añadir el libro:", error);
        //     });
        // });
        btnAgregarLibro.addEventListener("click", function () {
            formAgregarLibro.style.display = "block";
        });
        
        btnCancelar.addEventListener("click", function () {
            formAgregarLibro.style.display = "none";
        });

    } else {
        console.error("No se encontró la cookie de sesión.");
    }
    
});










// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}