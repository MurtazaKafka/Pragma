import React from 'react';
import QueryInput from "./components/QueryInput";
import Header from "./components/Header";
import TagInput from "./components/TagInput";
import RecentChats from "./components/RecentChats";

const Landing = () => {
    return (
        <div
            className="font-inria-serif flex overflow-hidden flex-col items-center px-20 pt-40 pb-28 bg-stone-100 max-md:px-5 max-md:py-24 h-screen">
            <div className="flex flex-col justify-center items-center w-full gap-5">
                <Header/>
                <QueryInput/>
                <TagInput />
                <RecentChats />
            </div>
        </div>
    );
};

export default Landing;
