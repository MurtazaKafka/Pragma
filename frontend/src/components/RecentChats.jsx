import React from 'react';
import ChatItem from './ChatItem';

function RecentChats() {
    const chatItems = [
        { content: 'What is a maximum matching between college A\'s students and classes?' },
        { content: 'How many people have...' },
        { content: 'How much money...' },
    ];

    return (
        <div className="w-4/5 md:w-1/2 px-3.5 flex-col flex-wrap justify-center items-center mx-6 mb-64">
            <h2 className="font-bodoni mt-6 mb-4 text-2xl text-heliotrope-700">
                Recent Chats
            </h2>
            <div className="flex gap-5 max-md:flex-col text-md">
                    {chatItems.map((item, index) => (
                        <ChatItem key={index} content={item.content} />
                    ))}
            </div>
        </div>
    );
}

export default RecentChats;