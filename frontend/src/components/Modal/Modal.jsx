import React from "react";
import CsvTable from "../CsvTable/CsvTable";
import './Modal.css';

const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null; // Don't render the modal if isOpen is false
  
    return (
       <div className="modal-overlay" onClick={onClose}>
         <div className="modal-content" onClick={(e) => e.stopPropagation()}>
           <button className="close-button" onClick={onClose}>
              <i className="fa fa-download"></i>
            </button>
           <CsvTable/>
           {children}
         </div>
       </div>
    );
  };
  
  export default Modal;