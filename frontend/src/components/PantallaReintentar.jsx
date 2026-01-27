import React, { useEffect, useState } from 'react';
import '../App.css';

export default function PantallaReintentar({ alClickCasa, alIntentarDeNuevo }) {
    const [animacionActiva, setAnimacionActiva] = useState(false);

    useEffect(() => {
        setAnimacionActiva(true);
    }, []);

    return (
        <div className={`pantalla-resultado pantalla-reintentar ${animacionActiva ? 'activa' : ''}`}>
            <div className="resultado-contenido">
                <div className="icono-resultado icono-reintentar">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="10" fill="#f59e0b"/>
                        <path d="M12 8v4l2 2" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                </div>

                <h1 className="titulo-resultado titulo-reintentar">Casi lo logras!</h1>

                <div className="mensaje-motivacional">
                    <p className="mensaje-resultado">La oracion no coincidio con tu pronunciacion.</p>
                    <p className="tip-resultado">Tip: Habla claro y despacio frente al microfono</p>
                </div>

                <div className="botones-resultado">
                    <button className="btn-resultado btn-reintentar-principal" onClick={alIntentarDeNuevo}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                            <path d="M21 3v5h-5"/>
                            <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                            <path d="M8 16H3v5"/>
                        </svg>
                        <span>Intentar de nuevo</span>
                    </button>

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
