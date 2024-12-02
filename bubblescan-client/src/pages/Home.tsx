import React from 'react';
import Hero from '../components/Homehero';
import '../styles/App.css';

const Home: React.FC = () => {
    return (
        <div className="home">
            <main className="main-content">
                <Hero />
            </main>
        </div>
    );
};

export default Home;
