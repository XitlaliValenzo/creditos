document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.querySelector('form');
    formulario.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevenir envío para validar primero

        if (validarFormulario()) {
            formulario.submit(); // Enviar si todo es válido
        }
    });

    function validarFormulario() {
        let valido = true;
        let mensajesError = [];

        // Validar nombre del cliente
        const cliente = document.getElementById('cliente');
        if (!cliente.value.trim()) {
            mensajesError.push('El nombre del cliente es requerido');
            valido = false;
        }

        // Validar monto 
        const monto = document.getElementById('monto');
        if (!monto.value) {
            mensajesError.push('El monto es requerido');
            valido = false;
        } else if (parseFloat(monto.value) <= 0) {
            mensajesError.push('El monto debe ser mayor a 0');
            valido = false;
        }

        // Validar tasa de interés
        const tasaInteres = document.getElementById('tasa_interes');
        if (!tasaInteres.value) {
            mensajesError.push('La tasa de interés es requerida');
            valido = false;
        } else if (parseFloat(tasaInteres.value) <= 0 || parseFloat(tasaInteres.value) > 100) {
            mensajesError.push('La tasa debe estar entre 0.01 y 100');
            valido = false;
        }

        // Validar plazo en meses
        const plazo = document.getElementById('plazo');
        if (!plazo.value) {
            mensajesError.push('El plazo es requerido');
            valido = false;
        } 

        // Validar fecha de otorgamiento
        const fechaOtorgamiento = document.getElementById('fecha_otorgamiento');
        if (!fechaOtorgamiento.value) {
            mensajesError.push('La fecha es requerida');
            valido = false;
        }

        // Mensajes de errores
        if (mensajesError.length > 0) {
            alert("Errores en el formulario:\n\n" + mensajesError.join("\n"));
        }

        return valido;
    }
});