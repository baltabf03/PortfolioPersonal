//BOTON DE VOLVER AL INDICE
const scrollButton= document.getElementById('boton-indice');
const scrollThreshold = 100;

window.addEventListener('scroll', ()=> {
    if(window.scrollY > scrollThreshold) {
        scrollButton.style.display= "block";
    } else {
        scrollButton.style.display= "none"
    }
});

scrollButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

//FOOTER CON FECHA
const fechaActual= document.getElementById('fecha-actual');
const fecha= new Date();
const opciones= {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
fechaActual.textContent=fecha.toLocaleDateString('es-AR', opciones)

//EXPANDIR CONTENIDO
function ConfigurarVerMas(botonId, selectorElementos){
    const boton= document.getElementById(botonId);
    const elementos= document.querySelectorAll(selectorElementos);
    let expandido= false;

    boton.addEventListener('click', ()=>{
        expandido= !expandido;

        elementos.forEach(el => el.classList.toggle('mostrar'));
        boton.textContent= expandido ? 'Ver menos' : 'Ver mas';
    });
}
ConfigurarVerMas('boton-Ver_Mas','.extra');
ConfigurarVerMas('boton-Ver_Testimonios','.extra')

//VALIDACION DEL FORMULARIO
function verificar_form() {
    const form= document.getElementById('datos-form');
    const divDatos= document.getElementById('datos-guardados')

    const valorNumero= form.elements.numero.value.trim();
    const valorNombre= form.elements.nya.value.trim();
    const valorCorreo= form.elements.email.value.trim();

    if (valorNombre !== '' && valorNumero !== '' && valorCorreo !== '' && (valorCorreo.includes('@gmail') || valorCorreo.includes('@hotmail'))) {
        
        const usuario = {
            nombre: valorNombre,
            numero: valorNumero,
            correo: valorCorreo,
        };

        localStorage.setItem('usuario',JSON.stringify(usuario));
        divDatos.innerHTML= `
            <h3>Datos guardados:</h3>
            <p><strong>Nombre:</strong> ${usuario.nombre}</p>
            <p><strong>Numero:</strong> ${usuario.numero}</p>
            <p><strong>Correo:</strong> ${usuario.correo}</p>
        `;
    }
    else {
        alert('Datos invalidos.');
    }
}