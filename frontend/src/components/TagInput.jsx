import React from 'react';

function TagInput() {
    return (
        <form className="flex flex-wrap gap-5 justify-center items-center px-3.5 text-md text-black rounded-lg w-4/5 md:w-2/3 ">
            <label htmlFor="queryInput" className="sr-only">Enter Query</label>
            <textarea
                id="queryInput"
                type="text"
                placeholder="Search Organisations (comma-separated)"
                className="flex-grow p-2 h-fit border border-gray-300 rounded-md transition duration-500 hover:outline-none focus:outline-none hover:shadow-md"
                aria-label="Enter Organisations"
            />
        </form>
    );
}

export default TagInput;