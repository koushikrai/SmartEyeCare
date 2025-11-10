'use client'
import React from "react";

const Feedback = () => {
    const backgroundStyle = {
        backgroundImage: "url('/images/Eyeimage.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        padding: "40px 20px",
    };

    const containerStyle = {
        maxWidth: "900px",
        margin: "0 auto",
    };

    const cardStyle = {
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        padding: "30px",
        borderRadius: "15px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.3)",
        marginBottom: "30px",
    };

    const sectionTitleStyle = {
        color: "#007BFF",
        borderBottom: "3px solid #007BFF",
        paddingBottom: "10px",
        marginBottom: "20px",
    };

    const tipStyle = {
        backgroundColor: "#f8f9fa",
        padding: "15px",
        borderRadius: "8px",
        marginBottom: "15px",
        borderLeft: "4px solid #28a745",
    };

    return (
        <div style={backgroundStyle}>
            <div style={containerStyle}>
                <div style={cardStyle}>
                    <h1 className="text-center mb-4" style={{ color: "#007BFF" }}>
                        Feedback for the eye redness and preventive measure reduce possibility of myopia
                    </h1>
                    <p className="text-center text-muted mb-5">
                        Expert advice on managing eye redness and myopia
                    </p>
                </div>

                {/* Redness Remedies Section */}
                <div style={cardStyle}>
                    <h2 style={sectionTitleStyle}>🔴 How to Cure Eye Redness</h2>
                    
                    <div style={tipStyle}>
                        <h5><strong>1. Use Lubricating Eye Drops</strong></h5>
                        <p className="mb-0">
                            Artificial tears or lubricating eye drops can help soothe irritated eyes. 
                            Use preservative-free drops for frequent use. Apply 2-3 drops in each eye 
                            as needed throughout the day.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>2. Reduce Screen Time</strong></h5>
                        <p className="mb-0">
                            Follow the 20-20-20 rule: Every 20 minutes, look at something 20 feet 
                            away for 20 seconds. Take regular breaks from digital devices to prevent 
                            digital eye strain.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>3. Apply Cold Compress</strong></h5>
                        <p className="mb-0">
                            Place a clean, cold, damp cloth over your closed eyes for 10-15 minutes. 
                            This can help reduce inflammation and soothe redness. Repeat 2-3 times daily.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>4. Stay Hydrated</strong></h5>
                        <p className="mb-0">
                            Drink plenty of water throughout the day. Dehydration can cause dry eyes, 
                            leading to redness and irritation. Aim for 8-10 glasses of water daily.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>5. Improve Indoor Air Quality</strong></h5>
                        <p className="mb-0">
                            Use a humidifier in dry environments, especially during winter. Avoid 
                            direct exposure to fans or air conditioning blowing directly into your eyes.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>6. Get Adequate Sleep</strong></h5>
                        <p className="mb-0">
                            Ensure you get 7-9 hours of quality sleep each night. Lack of sleep can 
                            cause eye fatigue and redness. Maintain a consistent sleep schedule.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>7. Avoid Eye Rubbing</strong></h5>
                        <p className="mb-0">
                            Resist the urge to rub your eyes, as this can worsen irritation and 
                            introduce bacteria. If your eyes are itchy, use a clean, damp cloth instead.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>8. Consult an Eye Doctor</strong></h5>
                        <p className="mb-0">
                            If redness persists for more than a few days, is accompanied by pain, 
                            vision changes, or discharge, consult an ophthalmologist for proper diagnosis 
                            and treatment.
                        </p>
                    </div>
                </div>

                {/* Myopia Management Section */}
                <div style={cardStyle}>
                    <h2 style={sectionTitleStyle}>👓 Managing Myopia (Nearsightedness)</h2>
                    
                    <div style={tipStyle}>
                        <h5><strong>1. Wear Corrective Lenses</strong></h5>
                        <p className="mb-0">
                            If myopia is detected, get a comprehensive eye exam and wear prescribed 
                            glasses or contact lenses. Proper correction helps prevent eye strain and 
                            slows progression in children.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>2. Increase Outdoor Time</strong></h5>
                        <p className="mb-0">
                            Spend at least 2 hours per day outdoors in natural light. Studies show 
                            that outdoor activities can help slow myopia progression, especially 
                            in children aged 3-12 years.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>3. Practice Good Reading Habits</strong></h5>
                        <p className="mb-0">
                            Maintain proper reading distance (about 16-18 inches from your eyes). 
                            Ensure adequate lighting when reading or using digital devices. Avoid 
                            reading in dim light or while lying down.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>4. Limit Close-Up Work</strong></h5>
                        <p className="mb-0">
                            Take regular breaks from close-up activities (reading, writing, screen time). 
                            Follow the 20-20-20 rule and encourage children to play outdoors instead of 
                            excessive screen time.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>5. Consider Myopia Control Treatments</strong></h5>
                        <p className="mb-0">
                            For children with progressive myopia, discuss options with an eye care 
                            professional: orthokeratology (ortho-k) lenses, atropine eye drops, 
                            or specialized contact lenses designed to slow progression.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>6. Maintain Regular Eye Exams</strong></h5>
                        <p className="mb-0">
                            Schedule annual eye examinations, especially for children. Early detection 
                            and monitoring help manage myopia effectively and prevent complications 
                            like retinal detachment.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>7. Ensure Proper Nutrition</strong></h5>
                        <p className="mb-0">
                            Include foods rich in vitamin A, C, E, and omega-3 fatty acids in your diet. 
                            Leafy greens, fish, carrots, and citrus fruits support overall eye health.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>8. Monitor Screen Distance</strong></h5>
                        <p className="mb-0">
                            Keep digital devices at arm's length (about 20-26 inches away). Adjust 
                            font sizes and screen brightness to comfortable levels. Use blue light 
                            filters if needed.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>9. Eye Exercises (For Adults)</strong></h5>
                        <p className="mb-0">
                            While exercises won't reverse myopia, they can help reduce eye strain: 
                            focus on distant objects, practice eye rolling, and do palming exercises 
                            (cover eyes with palms) for relaxation.
                        </p>
                    </div>

                    <div style={tipStyle}>
                        <h5><strong>10. Professional Consultation</strong></h5>
                        <p className="mb-0">
                            If myopia is detected or progressing rapidly, consult an optometrist or 
                            ophthalmologist. They can provide personalized treatment plans and monitor 
                            your eye health regularly.
                        </p>
                    </div>
                </div>

                {/* General Tips Section */}
                <div style={cardStyle}>
                    <h2 style={sectionTitleStyle}>💡 General Eye Care Tips</h2>
                    <ul style={{ fontSize: "16px", lineHeight: "1.8" }}>
                        <li>Blink regularly, especially when using digital devices</li>
                        <li>Maintain a balanced diet with eye-healthy nutrients</li>
                        <li>Wear UV-protective sunglasses when outdoors</li>
                        <li>Avoid smoking, as it can worsen eye conditions</li>
                        <li>Keep your workspace well-lit and ergonomically set up</li>
                        <li>Stay active and maintain a healthy lifestyle</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Feedback;
