import React, {useState} from 'react';
import UpArrowIcon from "../common/UpArrowIcon";
import Modal from "./Modal/Modal"

function QueryInput() {
    const [query, setQuery] = useState('');

    const handleChange = (e) => {
        setQuery(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add your submit logic here
        console.log('Submitted:', query);
    };

    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <div>
            <form
                className="flex flex-wrap gap-5 justify-center items-center px-3.5 text-lg text-black rounded-lg"
                onSubmit={handleSubmit}>
                <label htmlFor="queryInput" className="sr-only">Enter Query</label>

                <div className="relative w-full">
                    {query && (
                        <button
                            type="submit"
                            className="absolute top-7 -right-14 bg-transparent text-white rounded px-3 py-1 transition-opacity duration-1000"
                            onClick={openModal}
                        >
                            <UpArrowIcon />
                        </button>
                    )}
                </div>
                <textarea
                    id="queryInput"
                    value={query}
                    style={{
                        maxHeight: '500px',  // Set max height
                        overflowY: query ? 'auto' : 'hidden',  // Show scrollbar only when there's text
                        height: 'auto',  // Allow the height to be dynamic
                        resize: 'none',
                    }}
                    onChange={handleChange}
                    placeholder="What would you like to know?"
                    className="flex-grow p-2 h-fit border border-gray-300 rounded-md transition duration-500 hover:outline-none focus:outline-none hover:shadow-md"
                    aria-label="Enter Query"
                    rows={3}
                />

            </form>
            <Modal isOpen={isModalOpen} onClose={closeModal}></Modal>
        </div>
    );
}

export default QueryInput;