import React, { useState } from 'react';
import { Send } from 'lucide-react';

function QueryInput({ onSubmit }) {
    const [query, setQuery] = useState('');
    const [organisations, setOrganisations] = useState('');

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleOrganisationsChange = (e) => {
        setOrganisations(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const organisationsList = organisations
            .split(',')
            .map(org => org.trim())
            .filter(org => org.length > 0);
            
        const questions = query
            .split(',')
            .map(q => q.trim())
            .filter(q => q.length > 0);
            
        onSubmit({
            questions: questions,
            organizations: organisationsList
        });
    };

    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <div className="w-full md:w-full bg-white rounded-xl shadow-lg p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                    <label 
                        htmlFor="queryInput" 
                        className="block text-lg font-bold text-heliotrope-700"
                    >
                        Questions
                    </label>
                    <div className="relative">
                        <textarea
                            id="queryInput"
                            value={query}
                            onChange={handleQueryChange}
                            placeholder="What would you like to know? (newline-separated questions)"
                            className="font-bodoni resize-none w-full min-h-[120px] p-4 text-heliotrope-800 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ease-in-out"
                            rows={3}
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <label 
                        htmlFor="organisationsInput" 
                        className="block text-lg font-bold text-gray-700"
                    >
                        Organizations
                    </label>
                    <div className="relative">
                        <textarea
                            id="organisationsInput"
                            value={organisations}
                            onChange={handleOrganisationsChange}
                            placeholder="Enter organizations (comma-separated)"
                            className="font-bodoni w-full p-4 text-heliotrope-800 border border-gray-200 rounded-lg bg-gray-50 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ease-in-out resize-none"
                            rows={2}
                        />
                    </div>
                </div>

                <div className="flex justify-end mt-4">
                    <button
                        type="submit"
                        className="inline-flex items-center px-3 py-3 bg-heliotrope-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors duration-200"
                    >
                        {/* <span className="mr-2">Submit</span> */}
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default QueryInput;