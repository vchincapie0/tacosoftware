const hamBurger = document.querySelector(".toggle-btn");
hamBurger.addEventListener("click", function () {
document.querySelector("#sidebar").classList.toggle("expand");
});

// logout.js
window.addEventListener('beforeunload', function (e) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/logout/', false);
    xhr.send();
});

var sessionTimeout;

// Función para restablecer el temporizador de inactividad
function resetSessionTimeout() {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(function() {
        // Cuando se alcanza el tiempo de expiración de sesión, enviar una solicitud para cerrar la sesión
        fetch('/logout/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(function(response) {
            if (response.ok) {
                // Redirigir al usuario a la página de inicio de sesión
                window.location.href = '/login/';
            }
        }).catch(function(error) {
            console.error('Error al cerrar sesión:', error);
        });
    }, 1800000); // 30 minutos en milisegundos
}

// Restablecer el temporizador cuando se detecte actividad del usuario
document.addEventListener('mousemove', resetSessionTimeout);
document.addEventListener('keypress', resetSessionTimeout);

// Iniciar el temporizador cuando se carga la página
resetSessionTimeout();

