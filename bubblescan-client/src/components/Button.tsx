import React from 'react';
import '../styles/Button.css';

interface ButtonProps {
    text: string;
    dark?: boolean;
}

const Button: React.FC<ButtonProps> = ({ text, dark = false }) => {
    return (
        <button className={`button ${dark ? 'button-dark' : 'button-light'}`}>
            {text}
        </button>
    );
};

export default Button;
