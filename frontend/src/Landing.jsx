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
        <div className="min-h-screen bg-gradient-to-b from-heliotrope-50 to-heliotrope-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="space-y-8">
                    <Header />
                    <div className="flex justify-center">
                        <div className="max-w-3xl mx-auto md:w-1/2">
                            <QueryInput onSubmit={handleQuerySubmit} />
                        </div>
                    </div>
                    {queryData && (
                        <div className="mt-8">
                            <CSVViewer initialData={queryData} />
                        </div>
                    )}
                    <div className="mt-8 flex justify-center">
                        <RecentChats />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Landing;