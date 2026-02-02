import React from 'react';
import './Modal.css';

/**
 * Componente Modal reutilizable
 * @param {boolean} mostrar - Controla si el modal está visible
 * @param {function} onCerrar - Función para cerrar el modal
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje principal
 * @param {string} tipo - Tipo de modal: 'error', 'exito', 'advertencia', 'info'
 * @param {string} textoBoton - Texto del botón (opcional, por defecto "OK")
 */
const Modal = ({
    mostrar,
    onCerrar,
    titulo = "Mensaje",
    mensaje,
    tipo = "info",
    textoBoton = "OK",
    children
}) => {
    if (!mostrar) return null;

    // Íconos según el tipo
    const iconos = {
        error: "❌",
        exito: "✅",
        advertencia: "⚠️",
        info: "ℹ️"
    };

    return (
        <div className="modal-overlay" onClick={onCerrar}>
            <div
                className={`modal-contenido modal-${tipo}`}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="modal-header">
                    <span className="modal-icono">{iconos[tipo]}</span>
                    <h2 className="modal-titulo">{titulo}</h2>
                </div>

                <div className="modal-body">
                    {mensaje && <p className="modal-mensaje">{mensaje}</p>}
                    {children}
                </div>

                <div className="modal-footer">
                    <button
                        className="modal-boton"
                        onClick={onCerrar}
                    >
                        {textoBoton}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Modal;
