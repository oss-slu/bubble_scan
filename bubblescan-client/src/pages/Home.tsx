import React from 'react';
import Header from '../components/Header';
import Hero from '../components/Homehero';
import Footer from '../components/Footer';
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
