import React, { useEffect, useState } from 'react';
import '../App.css';

export default function PantallaError({ alClickCasa, alContinuar, respuestaCorrecta, tipoJuego, intentos }) {
    const [animacionActiva, setAnimacionActiva] = useState(false);

    useEffect(() => {
        setAnimacionActiva(true);
    }, []);

    // Si ya agotó los intentos (3), mostrar pantalla diferente
    const agotoIntentos = intentos >= 3;

    return (
        <div className={`pantalla-resultado pantalla-error ${animacionActiva ? 'activa' : ''}`}>
            <div className="resultado-contenido">
                <div className={`icono-resultado ${agotoIntentos ? 'icono-info' : 'icono-error'}`}>
                    {agotoIntentos ? (
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="10" fill="#f59e0b"/>
                            <path d="M12 8v4M12 16h.01" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                        </svg>
                    ) : (
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="10" fill="#ef4444"/>
                            <path d="M15 9l-6 6M9 9l6 6" stroke="white" strokeWidth="2.5" strokeLinecap="round"/>
                        </svg>
                    )}
                </div>

                <h1 className={`titulo-resultado ${agotoIntentos ? 'titulo-info' : 'titulo-error'}`}>
                    {agotoIntentos ? 'Sigue practicando!' : 'Intentalo de nuevo!'}
                </h1>

                <div className="respuesta-correcta-card">
                    <p className="label-respuesta">La palabra era:</p>
                    <p className="palabra-correcta">{respuestaCorrecta}</p>
                </div>

                {!agotoIntentos && (
                    <div className="intentos-restantes">
                        <p>Intentos: {intentos} de 3</p>
                        <div className="barra-intentos">
                            <div className="barra-progreso" style={{ width: `${(intentos / 3) * 100}%` }}></div>
                        </div>
                    </div>
                )}

                <div className="botones-resultado">
                    {agotoIntentos ? (
                        <button className="btn-resultado btn-continuar-error" onClick={alContinuar}>
                            <span>Siguiente palabra</span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="m9 18 6-6-6-6"/>
                            </svg>
                        </button>
                    ) : (
                        <button className="btn-resultado btn-reintentar" onClick={alContinuar}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                                <path d="M21 3v5h-5"/>
                                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                                <path d="M8 16H3v5"/>
                            </svg>
                            <span>Intentar de nuevo</span>
                        </button>
                    )}

                    <button className="btn-resultado btn-home-secundario" onClick={alClickCasa}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                            <polyline points="9 22 9 12 15 12 15 22"/>
                        </svg>
                        <span>Ir al inicio</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
