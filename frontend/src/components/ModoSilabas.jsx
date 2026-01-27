import React, { useState, useEffect } from 'react';
import '../App.css';
import PantallaCorrecta from './PantallaCorrecta';
import PantallaError from './PantallaError';

function ModoSilabas({ palabras, indice, alClickCasa, alClickOracion }) {
    const [opcionSeleccionada, setOpcionSeleccionada] = useState(null);
    const [mostrarExito, setMostrarExito] = useState(false);
    const [mostrarError, setMostrarError] = useState(false);
    const [intentos, setIntentos] = useState(0);
    const [opcionesAleatorias, setOpcionesAleatorias] = useState([]);

    const palabraActual = palabras[indice];

    // Mezclar opciones cuando cambia la palabra
    useEffect(() => {
        if (palabraActual && palabraActual.opciones) {
            const opcionesMezcladas = [...palabraActual.opciones].sort(() => Math.random() - 0.5);
            setOpcionesAleatorias(opcionesMezcladas);
            setOpcionSeleccionada(null);
            setMostrarExito(false);
            setMostrarError(false);
        }
    }, [palabraActual]);

    if (!palabraActual) return <div className="screen">Cargando juego...</div>;

    // Obtener la sílaba correcta
    const silabaCorrecta = palabraActual.silabas[palabraActual.silaba_oculta];

    // Construir la palabra con el espacio en blanco
    const renderizarPalabraConEspacio = () => {
        return palabraActual.silabas.map((silaba, idx) => {
            if (idx === palabraActual.silaba_oculta) {
                return (
                    <span key={idx} className="silaba-oculta">
                        {opcionSeleccionada || '___'}
                    </span>
                );
            }
            return <span key={idx} className="silaba-visible">{silaba}</span>;
        });
    };

    const seleccionarOpcion = (opcion) => {
        setOpcionSeleccionada(opcion);
    };

    const comprobarRespuesta = () => {
        if (opcionSeleccionada === silabaCorrecta) {
            setMostrarExito(true);
        } else {
            setIntentos(intentos + 1);
            setMostrarError(true);
        }
    };

    const continuarDespuesDeExito = () => {
        setMostrarExito(false);
        setOpcionSeleccionada(null);
        alClickOracion();
    };

    const continuarDespuesDeError = () => {
        setMostrarError(false);

        if (intentos >= 3) {
            alClickOracion();
        } else {
            setOpcionSeleccionada(null);
            // Remezclar opciones
            const opcionesMezcladas = [...palabraActual.opciones].sort(() => Math.random() - 0.5);
            setOpcionesAleatorias(opcionesMezcladas);
        }
    };

    // Manejo de teclado para accesibilidad
    const manejarTeclaOpcion = (e, opcion) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            seleccionarOpcion(opcion);
        }
    };

    // Mostrar pantalla de éxito
    if (mostrarExito) {
        return <PantallaCorrecta alContinuar={continuarDespuesDeExito} />;
    }

    // Mostrar pantalla de error
    if (mostrarError) {
        return (
            <PantallaError
                alClickCasa={alClickCasa}
                alContinuar={continuarDespuesDeError}
                respuestaCorrecta={palabraActual.nombre}
                tipoJuego="silabas"
                intentos={intentos}
            />
        );
    }

    return (
        <div id="syllables-game-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <div className="progress-counter top-center">
                {indice + 1}/{palabras.length}
            </div>

            <div className="content-center">
                <div className="image-container">
                    <img src={palabraActual.imagen} alt="Referencia visual" className="game-image"/>
                </div>

                <div className="game-card-white">
                    <p className="syllables-instruction">Completa la palabra eligiendo la silaba correcta:</p>

                    <div className="word-display">
                        {renderizarPalabraConEspacio()}
                    </div>

                    <div className="syllables-options">
                        {opcionesAleatorias.map((opcion, idx) => (
                            <button
                                key={idx}
                                className={`syllable-option ${opcionSeleccionada === opcion ? 'selected' : ''}`}
                                onClick={() => seleccionarOpcion(opcion)}
                                onKeyDown={(e) => manejarTeclaOpcion(e, opcion)}
                                tabIndex="0"
                                aria-label={`Seleccionar silaba ${opcion}`}
                            >
                                {opcion}
                            </button>
                        ))}
                    </div>

                    {opcionSeleccionada && (
                        <div id="check-button-container">
                            <button className="btn-check game-card-btn" onClick={comprobarRespuesta}>
                                Comprobar
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ModoSilabas;
