import React from 'react';
import Header from './components/Header';
import QueryInput from './components/QueryInput';

function AboutPage() {
    return (
        <main className="flex overflow-hidden flex-col items-center">
            <div className="flex flex-col">
                <Header />
                <QueryInput />
            </div>
        </main>
    );
}

export default AboutPage;