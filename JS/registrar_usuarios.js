document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registroForm").addEventListener("submit", function (event) {
        event.preventDefault(); 

       
        let nombre = document.getElementById("nombre").value;
        
        let password = document.getElementById("password").value;

        
        fetch("http://127.0.0.1:5000/usuario/registrar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nombre,password })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("mensaje").innerText = data.mensaje || data.error;
        })
        .catch(error => console.error("Error:", error));
    });
});