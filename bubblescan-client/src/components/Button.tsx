import React from 'react';
import '../styles/Button.css';
import { useNavigate } from 'react-router-dom';

interface ButtonProps {
    text: string;
    dark?: boolean;
    to?: string;
}

const Button: React.FC<ButtonProps> = ({ text, dark = false, to }) => {

    const navigate = useNavigate();

    const handleClick = () => {
        if (to) {
            navigate(to);
        }
    };

    return (
        <button className={`button ${dark ? 'button-dark' : 'button-light'}`}
            onClick={handleClick}
        >
            {text}
        </button>
    );
};

export default Button;
