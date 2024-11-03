import React from 'react';

function ChatItem({ content }) {
    return (
        <article className="flex flex-col w-[33%] max-md:ml-0 max-md:w-full">
            {content ? (
                <div className="grow px-3 pt-1.5 pb-2 w-full text-md rounded-lg bg-zinc-300 max-md:px-5 max-md:mt-9">
                    {content}
                </div>
            ) : (
                <div className="flex shrink-0 mx-auto rounded-lg bg-zinc-300 h-[125px] w-[200px] max-md:mt-9" />
            )}
        </article>
    );
}

export default ChatItem;