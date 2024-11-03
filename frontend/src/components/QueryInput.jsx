import React, {useState} from 'react';
import UpArrowIcon from "../common/UpArrowIcon";
import Modal from "./Modal/Modal"

function QueryInput() {
    const [query, setQuery] = useState('');
    const [organisations, setOrganisations] = useState('');

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleOrganisationsChange = (e) => {
        setOrganisations(e.target.value);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add your submit logic here
        console.log('Submitted:', query);
        console.log('Submitted:', organisations);
    };

    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <>
    <form
        className="flex flex-wrap gap-5 justify-center items-center px-3.5 text-lg text-black rounded-lg w-4/5 md:w-1/2"
        onSubmit={handleSubmit}>
        <label htmlFor="queryInput" className="sr-only">Enter Query</label>
                <div className="relative w-full">
                    {query && (
                        <button
                            type="submit"
                            className="absolute top-7 -right-14 bg-transparent text-white rounded px-3 py-1 transition-opacity duration-200"
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
                        //height: 'auto',  // Allow the height to be dynamic
                        height: '10rem',
                        resize: 'none',
                        borderRadius: "1rem",
                    }}
                    onChange={handleQueryChange}
                    placeholder="What would you like to know? Type each query on a new line."
                    className="text-base font-bodoni placeholder-heliotrope-300 text-heliotrope-600 flex-grow p-2 pl-3 pr-3 h-fit border border-gray-300
                    rounded-md transition duration-500 hover:outline-none focus:outline-none hover:shadow-md"
                    aria-label="Enter Query"
                    rows={3}
                />

    </form>
    <form
        className="flex flex-wrap gap-5 justify-center items-center px-3.5 text-md text-black rounded-lg w-4/5 md:w-1/2 ">
        <label htmlFor="queryInput" className="sr-only">Enter Query</label>
        <textarea
            id="queryInput"
            type="text"
            onChange={handleOrganisationsChange}
            placeholder="Enter organizations, separated by commas."
            className="text-base font-bodoni placeholder-font-bodoni placeholder-heliotrope-300 text-heliotrope-600 pl-3 pr-3 flex-grow p-2 h-fit border border-gray-300 rounded-md transition duration-500 hover:outline-none focus:outline-none hover:shadow-md"
            aria-label="Enter Organisations"
            style={{
                resize: 'none',
                borderRadius: '1rem',
            }}
        />
    </form>
    <Modal isOpen={isModalOpen} onClose={closeModal}></Modal>
        </>
    );
}

export default QueryInput;