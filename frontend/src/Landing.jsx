import React, { useState } from 'react';
import ReactDOM from "react-dom";
import QueryInput from "./components/QueryInput";
import Header from "./components/Header";
import TagInput from "./components/TagInput";
import RecentChats from "./components/RecentChats";
import Modal from "./components/Modal/Modal"

const Landing = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <div>
            <div className="font-inria-serif flex overflow-hidden flex-col items-center px-20 pt-40 pb-28 bg-stone-100 max-md:px-5 max-md:py-24 h-screen">
                <div className="flex flex-col justify-center items-center w-full gap-5">
                    <Header/>
                    <QueryInput/>
                    <TagInput />
                    <RecentChats />
                </div> 
            </div>
            {/* <button onClick={openModal}>
                <i className="fa fa-download"></i>
            </button>
            <Modal isOpen={isModalOpen} onClose={closeModal}></Modal> */}
        </div>
    );
};

export default Landing;
