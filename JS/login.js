document.addEventListener("DOMContentLoaded", function () {
    
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault(); 

        
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        
        if (!username || !password) {
            document.getElementById("mensaje").innerText = "Por favor, completa todos los campos.";
            return;
        }

        
        fetch("http://127.0.0.1:5000/usuario/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password }),
            credentials: "include" 
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                
                document.getElementById("mensaje").innerText = data.mensaje;
                setTimeout(() => {
                    window.location.href = "index.html"; 
                }, 1000);
            } else {
                
                document.getElementById("mensaje").innerText = data.error;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("mensaje").innerText = "Ocurrió un error al iniciar sesión.";
        });
    });
});