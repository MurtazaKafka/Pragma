import React, { useState } from 'react';
import QueryInput from "./components/QueryInput";
import Header from "./components/Header";
import RecentChats from "./components/RecentChats";
import CSVViewer from './components/CSVViewer';

const Landing = () => {
    const [queryData, setQueryData] = useState(null);

    const handleQuerySubmit = async (data) => {
        setQueryData(data);
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-stone-50 to-stone-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="space-y-8">
                    <Header />
                    <div className="max-w-3xl mx-auto">
                        <QueryInput onSubmit={handleQuerySubmit} />
                    </div>
                    {queryData && (
                        <div className="mt-8">
                            <CSVViewer initialData={queryData} />
                        </div>
                    )}
                    <div className="mt-8">
                        <RecentChats />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Landing;