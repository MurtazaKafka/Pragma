// Login.js
import React, {useState} from 'react';
import {useNavigate} from "react-router-dom";

const Register = () => {
    const REGISTER_URL = 'http://localhost:3001/register';
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });
    const [newUser, setNewUser] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(REGISTER_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
                credentials: 'include', // Include cookies in the request
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess(data.message);
                setError('');
                navigate('/login');
            } else {
                setError(data.message);
                setSuccess('');
            }
        } catch (error) {
            setError('An error occurred. Please try again.');
            setSuccess('');
        }
    };

    const navigate = useNavigate();

    return (
        <form
            noValidate
            className="flex w-full flex-col justify-center space-y-5 bg-white px-12 py-12 w-[25rem] rounded-2xl shadow-md"
        >
            <h1 className="text-2xl font-bold text-center">Welcome to Data Vault!</h1>
            <div className="flex flex-col justify-center gap-3">
                <label>
                    <div className="mb-1">Name</div>
                    <input
                        type="text"
                        name="name"
                        placeholder="Name"
                        onChange={handleChange}
                        value={formData.name}
                        required
                        className="shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </label>
                <label>
                    <div className="mb-1">Email</div>
                    <input
                        type="email"
                        name="email"
                        placeholder="Email address"
                        onChange={handleChange}
                        value={formData.email}
                        required
                        className="hadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"

                    />
                </label>
                <div className="">
                    <div className="mb-1">Password</div>
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                        className="shadow-sm rounded-md mb-2 w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                </div>
            </div>

            <div className="flex flex-col">

                <button onClick={handleSubmit} className="border mb-4 border-blue-600 bg-blue-600 rounded-md h-10 text-white">
                    Sign up
                </button>
                <button onClick={() => navigate('/login')}
                        className="text-center mb-1 text-md hover:text-blue-600 hover:underline">
                    Already have an account? Login
                </button>

            </div>
        </form>

    );
};

export default Register;

