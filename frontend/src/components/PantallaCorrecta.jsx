import React, { useEffect, useState } from 'react';
import '../App.css';

export default function PantallaCorrecta({ alContinuar }) {
    const [animacionActiva, setAnimacionActiva] = useState(false);

    useEffect(() => {
        // Activar animación al montar
        setAnimacionActiva(true);

        // Auto-continuar después de 2 segundos (opcional)
        const timer = setTimeout(() => {
            // Si quieres auto-continuar, descomenta: alContinuar();
        }, 2000);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className={`pantalla-resultado pantalla-exito ${animacionActiva ? 'activa' : ''}`}>
            {/* Confeti animado */}
            <div className="confeti-container">
                {[...Array(20)].map((_, i) => (
                    <div key={i} className={`confeti confeti-${i % 5}`} style={{
                        left: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 0.5}s`
                    }}></div>
                ))}
            </div>

            <div className="resultado-contenido">
                <div className="icono-resultado icono-exito">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="10" fill="#10b981"/>
                        <path d="M8 12l2.5 2.5L16 9" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                </div>

                <h1 className="titulo-resultado titulo-exito">Excelente!</h1>
                <p className="mensaje-resultado">Has completado la palabra correctamente</p>

                <div className="estrellas-container">
                    <span className="estrella">*</span>
                    <span className="estrella">*</span>
                    <span className="estrella">*</span>
                </div>

                <button className="btn-resultado btn-exito" onClick={alContinuar}>
                    <span>Continuar</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </button>
            </div>
        </div>
    );
}
