import React from "react";
import '../styles/content.css';
import CustomExamSheetComponent from '../components/CustomExamSheetComponent'

const Customsheet: React.FC = () => {
    return (
        <div className="Container">
            <h1 className="title">Custom  Sheet</h1>
            <div className="description">
                <CustomExamSheetComponent />
            </div>
        </div>
    );
};

export default Customsheet;
