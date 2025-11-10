'use client'
import React, { useState } from "react";

const Feedback = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");

    const backgroundStyle = {
        backgroundImage: "url('https://shreeretinacare.com/wp-content/uploads/2024/04/anatomy-inspired-abstract-design-with-futuristic-elements-generative-ai-2048x1170.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        padding: "40px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    };

    const formCardStyle = {
        backgroundColor: "rgba(255, 255, 255, 0.9)",
        padding: "30px",
        borderRadius: "10px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.2)",
        width: "100%",
        maxWidth: "600px",
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle form submission logic here
        console.log({ name, email, message });
    };

    return (
        <div style={backgroundStyle}>
            <div style={formCardStyle}>
                <h2 className="text-center mb-4">Feedback</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="name" className="form-label">Name</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            id="name" 
                            placeholder="Enter your name" 
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email</label>
                        <input 
                            type="email" 
                            className="form-control" 
                            id="email" 
                            placeholder="Enter your email" 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="message" className="form-label">Message</label>
                        <textarea 
                            className="form-control" 
                            id="message" 
                            rows="4" 
                            placeholder="Enter your feedback"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        ></textarea>
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default Feedback;
