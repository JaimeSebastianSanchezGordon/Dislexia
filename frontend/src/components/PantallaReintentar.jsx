import React from 'react';
import '../App.css';

function PantallaReintentar({ alClickCasa, alIntentarDeNuevo }) {
    return (
        <div id="retry-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>
            <div className="content-center">
                <div className="retry-icon">👍</div>
                <h1 className="title retry-title">¡Casi!</h1>
                <div className="retry-card">
                    <p className="retry-text">
                        ¡Oh no! La oración no es igual. Intenta leerla de nuevo exactamente como aparece.
                    </p>
                </div>
                <button className="btn-retry game-card-btn" onClick={alIntentarDeNuevo}>
                    Intentar de nuevo
                </button>
            </div>
        </div>
    );
}

export default PantallaReintentar;
