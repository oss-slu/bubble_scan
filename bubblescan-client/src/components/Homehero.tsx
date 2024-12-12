import React from 'react';
import Button from './Button';
import '../styles/Homehero.css';

const Homehero: React.FC = () => {
    return (
        <section className="hero">
            <h1 className="hero-title">Bubble Scan</h1>
            <p className="hero-subtitle">Grading Made Easy</p>
            <div className="hero-buttons">
                <Button text="Scan" to="/scan" />
                <Button text="Custom Sheets" dark to="/customsheets" />
            </div>
            <div className="hero-description">
                <h2>Bubble Scan</h2>
                <p>
                    This project automates the scanning of Scantron documents and the extraction of data to CSV files using a web-based application.
                    Users can upload scanned images of their Scantron forms, which are then processed by our backend AI algorithms to generate and
                    retrieve CSV files containing the extracted data. This system is designed for educational institutions and testing centers to
                    streamline their grading processes and data management.
                </p>
            </div>
        </section>
    );
};

export default Homehero;
