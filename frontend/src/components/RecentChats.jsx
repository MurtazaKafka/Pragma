import React from 'react';
import ChatItem from './ChatItem';

function RecentChats() {
    const chatItems = [
        { content: 'Has the college stopped education due to Hurricane Helene?' },
        { content: 'Was the bank affected by the recent bankruptancy?' },
        { content: 'When did the institution make their voting announcement?' },
    ];

    return (
        <div className="w-4/5 md:w-1/2 px-3.5 flex-col flex-wrap justify-center items-center mx-6">
            <div className='flex gap-2 items-center'>
                <i class="fa fa-database text-xl mb-4 text-heliotrope-700" style={{ alignSelf: 'flex-end' }}></i>
                <h2 className="font-bodoni mt-6 mb-4 text-2xl text-heliotrope-700">
                    Recent Datasets
                </h2>
            </div>
            <div className="flex gap-5 max-md:flex-col text-md justify-between">
                    {chatItems.map((item, index) => (
                        <ChatItem key={index} content={item.content} />
                    ))}
            </div>
        </div>
    );
}

export default RecentChats;