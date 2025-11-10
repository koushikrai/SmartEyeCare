'use client'
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

const Signup = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
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

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await axios.post("http://localhost:5000/signup", { email, password });
            router.push("/about");
        } catch (err) {
            setError("Signup failed. Email may already exist.");
        }
    };

    return (
        <div style={backgroundStyle}>
            <div style={formContainerStyle}>
                <h2 className="text-center mb-4">Sign Up</h2>
                {error && <div className="alert alert-danger" role="alert">{error}</div>}
                <form onSubmit={handleSignup}>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email address</label>
                        <input 
                            type="email" 
                            className="form-control" 
                            id="email" 
                            placeholder="Enter email" 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
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
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Sign Up</button>
                </form>
                <div className="text-center mt-3">
                    <span>Already have an account? </span>
                    <button
                        type="button"
                        className="btn btn-link p-0 align-baseline"
                        onClick={() => router.push('/')}
                    >
                        Login
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Signup;
