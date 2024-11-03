import React from "react";
import CsvTable from "../CsvTable/CsvTable";
import { handleDownload } from '../CsvTable/CsvTable';
import './Modal.css';

const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null; // Don't render the modal if isOpen is false
  
    return (
       <div className="modal-overlay" onClick={onClose}>
         <div className="modal-content bg-heliotrope-50" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={onClose}>
              <i className="text-2xl fa fa-times text-heliotrope-700 transition duration-200 hover:scale-110 hover:outline-none focus:outline-none"></i>
            </button>
            <button className="download-button" onClick={handleDownload}>
              <i className="text-2xl fa fa-download text-heliotrope-700 transition duration-200 hover:scale-110 hover:outline-none focus:outline-none"></i>  
            </button>
           <CsvTable/>
           {children}
         </div>
       </div>
    );
  };
  
  export default Modal;