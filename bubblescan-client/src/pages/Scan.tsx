import React from "react";
import "../styles/content.css";
import FileUploadComponent from '../components/FileUploadComponent'

const Scan: React.FC = () => {
    return (
        <div className="Container">
            <h1 className="title">Scan</h1>
            <div className="description">
                <FileUploadComponent />
            </div>

        </div>
    );
};

export default Scan;
