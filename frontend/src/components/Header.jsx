import React from 'react';

function Header() {
    return (
        <div className='flex gap-3'>
            <img src="full-logo.svg" alt="Logo" className="h-10 w-auto" />
            <header className="justify-center text-center text-4xl text-heliotrope-700 font-bodoni font-medium">
                Good Morning, User
            </header>
        </div>
    );
}

export default Header;