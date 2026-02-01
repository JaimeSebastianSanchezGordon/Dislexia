import React from 'react';
import '../App.css';

function PantallaError({ alClickCasa, alContinuar, respuestaCorrecta, tipoJuego, intentos }) {
    // Solo mostrar la respuesta correcta después del 3er intento
    const mostrarRespuesta = intentos >= 3;

    return (
        <div id="error-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>
            <div className="content-center">
                <div className="error-icon">😕</div>
                <h1 className="title">Fallaste</h1>
                <div className="error-card">
                    {mostrarRespuesta ? (
                        <>
                            <p className="error-text">No te preocupes, la forma correcta es:</p>
                            <p className="correct-answer">{respuestaCorrecta}</p>
                        </>
                    ) : (
                        <p className="error-text">¡Inténtalo de nuevo, tú puedes!</p>
                    )}
                </div>
                <button className="btn-error game-card-btn" onClick={alContinuar}>
                    {mostrarRespuesta ? 'Continuar' : 'Reintentar'}
                </button>
            </div>
        </div>
    );
}

export default PantallaError;
