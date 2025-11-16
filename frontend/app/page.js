'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const backgroundStyle = {
        backgroundImage: "url('/images/Eyeimage.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    };

    const formContainerStyle = {
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        padding: '40px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
        width: '400px',
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:5000/login', {
                email,
                password
            });

            if (response.data.message === 'Login successful') {
                // Store user info in localStorage (optional)
                localStorage.setItem('user', JSON.stringify({
                    email: response.data.email,
                    user_id: response.data.user_id
                }));
                router.push('/about');
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Login failed. Please try again.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={backgroundStyle}>
            <div style={formContainerStyle}>
                <h2 className="text-center mb-4">Login</h2>
                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email address</label>
                        <input 
                            type="email" 
                            className="form-control" 
                            id="email" 
                            placeholder="Enter email" 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input 
                            type="password" 
                            className="form-control" 
                            id="password" 
                            placeholder="Password" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button 
                        type="submit" 
                        className="btn btn-primary w-100"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
                <div className="text-center mt-3">
                    <span>Don't have an account? </span>
                    <button
                        type="button"
                        className="btn btn-link p-0 align-baseline"
                        onClick={() => router.push('/signup')}
                    >
                        Sign up
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Login;
