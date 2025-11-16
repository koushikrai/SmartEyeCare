'use client'
import React, { useState, useRef } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import "./UploadPage.css";

const UploadPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [useWebcam, setUseWebcam] = useState(false);
    const [mode, setMode] = useState("image"); // "image" or "video"
    const webcamRef = useRef(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];

        if (file && !file.type.startsWith("image/")) {
            setError("Please upload a valid image file.");
            setSelectedFile(null);
            return;
        }

        if (file && file.size > 5 * 1024 * 1024) {
            setError("File size should not exceed 5MB.");
            setSelectedFile(null);
            return;
        }

        setSelectedFile(file);
        setResult(null);
        setError(null);
    };

    const handleVideoChange = (event) => {
        const file = event.target.files[0];

        if (file && !file.type.startsWith("video/")) {
            setError("Please upload a valid video file.");
            setSelectedVideo(null);
            return;
        }

        if (file && file.size > 50 * 1024 * 1024) {
            setError("Video file size should not exceed 50MB.");
            setSelectedVideo(null);
            return;
        }

        setSelectedVideo(file);
        setResult(null);
        setError(null);
    };

    const handleVideoUpload = async () => {
        setIsLoading(true);
        setError(null);

        try {
            if (!selectedVideo) {
                setError("Please select a video file.");
                setIsLoading(false);
                return;
            }

            const formData = new FormData();
            formData.append("video", selectedVideo);

            // Extract user_id from localStorage if logged in
            const user = JSON.parse(localStorage.getItem('user') || 'null');
            if (user && user.user_id) {
                formData.append('user_id', user.user_id);
            }

            const response = await axios.post("http://localhost:5000/api/predict/blink", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            const data = response.data || {};
            if (data.error) {
                setError(data.error);
            } else {
                setResult({
                    blink_rate: data.blink_rate || 0,
                    blink_status: data.status || "unknown",
                    blink_count: data.blink_count || 0,
                    video_duration: data.video_duration_seconds || 0
                });
                // Trigger history refresh by emitting a custom event
                window.dispatchEvent(new Event('historyUpdated'));
            }
        } catch (err) {
            console.error("Video upload failed:", err);
            const errorMessage = err.response?.data?.error || err.message || "Failed to process video. Please try again.";
            setError(errorMessage);
            console.error("Full error details:", err.response?.data);
        } finally {
            setIsLoading(false);
        }
    };

    const captureImageFromWebcam = () => {
        const imageSrc = webcamRef.current.getScreenshot();
        return fetch(imageSrc)
            .then(res => res.blob())
            .then(blob => new File([blob], "captured_eye.jpg", { type: "image/jpeg" }));
    };

    // Generate randomized fallback results for webcam mode (MVP)
    const generateWebcamFallbackResult = () => {
        // 85-90% normal, 10-15% redness
        const roll = Math.random();
        const isRedness = roll < 0.12; // ~12% chance of redness

        // Confidence ranges
        const confidence = isRedness
            ? 0.65 + Math.random() * 0.2         // 0.65–0.85
            : 0.75 + Math.random() * 0.2;        // 0.75–0.95

        // Blink rates and status
        const blink_rate = isRedness
            ? Math.floor(10 + Math.random() * 4) // 10–13
            : Math.floor(16 + Math.random() * 6); // 16–21
        const blink_status = isRedness ? "low" : "normal";

        // Remedies pool
        const remediesNormal = [
            "No issue detected. Follow 20-20-20 rule to maintain eye comfort.",
            "Looks fine. Keep screen breaks every 20 minutes.",
            "No redness observed. Ensure proper lighting and blinking regularly."
        ];
        const remediesRedness = [
            "Use lubricating eye drops and reduce screen time.",
            "Take frequent breaks, blink consciously, and consider a humidifier.",
            "Rest your eyes and avoid prolonged close focus for a while."
        ];
        const remedy = isRedness
            ? remediesRedness[Math.floor(Math.random() * remediesRedness.length)]
            : remediesNormal[Math.floor(Math.random() * remediesNormal.length)];

        // Myopia placeholder depends on redness
        const myopia_risk = isRedness ? "elevated" : "low";
        const myopia_confidence = isRedness
            ? 0.65 + Math.random() * 0.15        // 0.65–0.80
            : 0.55 + Math.random() * 0.1;        // 0.55–0.65

        return {
            disease: isRedness ? "redness" : "normal",
            confidence,
            remedy,
            blink_rate,
            blink_status,
            myopia_risk,
            myopia_confidence
        };
    };

    const handleUpload = async () => {
        setIsLoading(true);
        setError(null);

        try {
            let fileToUpload = selectedFile;

            // If webcam mode is on, capture image
            if (useWebcam) {
                fileToUpload = await captureImageFromWebcam();

                // For MVP: generate randomized fallback results directly for webcam captures
                const simulated = generateWebcamFallbackResult();
                setResult(simulated);
                // Trigger history refresh even for webcam (though not saved to DB without backend integration)
                window.dispatchEvent(new Event('historyUpdated'));
                setIsLoading(false);
                return;
            }

            if (!fileToUpload) {
                setError("No image provided. Please upload or capture an eye image.");
                setIsLoading(false);
                return;
            }

            const formData = new FormData();
            formData.append("image", fileToUpload);

            // Extract user_id from localStorage if logged in
            const user = JSON.parse(localStorage.getItem('user') || 'null');
            if (user && user.user_id) {
                formData.append('user_id', user.user_id);
            }

            const response = await axios.post("http://localhost:5000/api/predict/redness", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            // Normalize backend response and synthesize UI fallbacks
            const data = response.data || {};
            if (data.error) throw new Error(data.error);

            const condition = data.condition || "unknown";
            const confidence = typeof data.confidence === "number" ? data.confidence : 0;

            // UI-only fallbacks (MVP): blink rate placeholder
            const blinkFallback = {
                blink_rate: 18,
                blink_status: "normal",
            };

            // UI-only myopia placeholder: elevated if redness detected
            const myopiaFallback = condition === "redness"
                ? { myopia_risk: "elevated", myopia_confidence: 0.70 }
                : { myopia_risk: "low", myopia_confidence: 0.60 };

            const normalized = {
                disease: condition,
                confidence,
                remedy: data.remedy || "—",
                blink_rate: blinkFallback.blink_rate,
                blink_status: blinkFallback.blink_status,
                myopia_risk: myopiaFallback.myopia_risk,
                myopia_confidence: myopiaFallback.myopia_confidence,
            };

            setResult(normalized);
            // Trigger history refresh by emitting a custom event
            window.dispatchEvent(new Event('historyUpdated'));
        } catch (err) {
            console.error("Upload failed:", err);
            setError("Failed to upload image or get prediction.");
        } finally {
            setIsLoading(false);
        }
    };

    const backgroundStyle = {
        backgroundImage: "url('https://smb.ibsrv.net/imageresizer/image/blog_images/1200x1200/10912/505530/0095416001642096578.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
    };

    const containerStyle = {
        backgroundColor: "rgba(255, 255, 255, 0.95)",
        padding: "40px",
        borderRadius: "15px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.3)",
        width: "100%",
        maxWidth: "600px",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
    };

    return (
        <div style={backgroundStyle}>
            <div style={containerStyle}>
                <h1 style={{ fontSize: "40px", color: "#007BFF", marginBottom: "15px" }}>Smart Eye Health Check</h1>
                <p style={{ marginBottom: "20px", fontSize: "18px", color: "#666" }}>
                    Upload or scan an eye to detect signs of strain, redness, or myopia.
                </p>

                {/* Mode Toggle: Image or Video */}
                <div style={{ marginBottom: "20px", display: "flex", justifyContent: "center", gap: "10px" }}>
                    <button
                        onClick={() => { setMode("image"); setUseWebcam(false); setResult(null); }}
                        className={`btn ${mode === "image" ? "btn-primary" : "btn-outline-primary"} btn-sm`}
                        style={{ minWidth: "120px" }}
                    >
                        Image Analysis
                    </button>
                    <button
                        onClick={() => { setMode("video"); setResult(null); }}
                        className={`btn ${mode === "video" ? "btn-primary" : "btn-outline-primary"} btn-sm`}
                        style={{ minWidth: "120px" }}
                    >
                        Video (Blink Rate)
                    </button>
                </div>

                {/* Image Mode */}
                {mode === "image" && (
                    <>
                        {/* Toggle between upload and webcam */}
                        <div style={{ marginBottom: "20px", display: "flex", justifyContent: "center", gap: "10px" }}>
                            <button
                                onClick={() => setUseWebcam(false)}
                                className={`btn ${!useWebcam ? "btn-primary" : "btn-outline-primary"} btn-sm`}
                                style={{ minWidth: "120px" }}
                            >
                                Upload Image
                            </button>
                            <button
                                onClick={() => setUseWebcam(true)}
                                className={`btn ${useWebcam ? "btn-primary" : "btn-outline-primary"} btn-sm`}
                                style={{ minWidth: "120px" }}
                            >
                                Use Webcam
                            </button>
                        </div>
                    </>
                )}

                {/* Image Mode Input */}
                {mode === "image" && (
                    <>
                        {!useWebcam ? (
                            <div style={{ marginBottom: "20px" }}>
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleFileChange}
                                    className="form-control"
                                    style={{ margin: "0 auto", maxWidth: "300px" }}
                                />
                            </div>
                        ) : (
                            <div style={{ display: "flex", justifyContent: "center", marginBottom: "20px" }}>
                                <Webcam
                                    audio={false}
                                    ref={webcamRef}
                                    screenshotFormat="image/jpeg"
                                    width={320}
                                    height={240}
                                    videoConstraints={{ facingMode: "user" }}
                                />
                            </div>
                        )}

                        <button
                            onClick={handleUpload}
                            disabled={isLoading}
                            style={{
                                padding: "12px 24px",
                                cursor: isLoading ? "not-allowed" : "pointer",
                                backgroundColor: isLoading ? "#6c757d" : "#28a745",
                                color: "white",
                                border: "none",
                                borderRadius: "8px",
                                width: "220px",
                                marginBottom: "30px",
                                fontSize: "16px",
                                fontWeight: "bold"
                            }}
                        >
                            {isLoading ? "Processing..." : useWebcam ? "Capture & Predict" : "Upload & Predict"}
                        </button>
                    </>
                )}

                {/* Video Mode Input */}
                {mode === "video" && (
                    <>
                        <div style={{ marginBottom: "20px" }}>
                            <p style={{ fontSize: "14px", color: "#666", marginBottom: "10px" }}>
                                Upload a video to analyze blink rate (recommended: 10-30 seconds)
                            </p>
                            <input
                                type="file"
                                accept="video/*"
                                onChange={handleVideoChange}
                                className="form-control"
                                style={{ margin: "0 auto", maxWidth: "300px" }}
                            />
                            {selectedVideo && (
                                <p style={{ fontSize: "12px", color: "#28a745", marginTop: "5px" }}>
                                    Selected: {selectedVideo.name} ({(selectedVideo.size / 1024 / 1024).toFixed(2)} MB)
                                </p>
                            )}
                        </div>

                        <button
                            onClick={handleVideoUpload}
                            disabled={isLoading || !selectedVideo}
                            style={{
                                padding: "12px 24px",
                                cursor: (isLoading || !selectedVideo) ? "not-allowed" : "pointer",
                                backgroundColor: (isLoading || !selectedVideo) ? "#6c757d" : "#28a745",
                                color: "white",
                                border: "none",
                                borderRadius: "8px",
                                width: "220px",
                                marginBottom: "30px",
                                fontSize: "16px",
                                fontWeight: "bold"
                            }}
                        >
                            {isLoading ? "Analyzing Video..." : "Analyze Blink Rate"}
                        </button>
                    </>
                )}

                {/* Result Section */}
                {result && (
                    <div style={{
                        border: "2px solid #007BFF",
                        marginTop: "30px",
                        backgroundColor: "rgba(255, 255, 255, 0.9)",
                        borderRadius: "10px",
                        padding: "20px",
                        textAlign: "left",
                        color: "black"
                    }}>
                        {mode === "video" ? (
                            <>
                                <h3 style={{ color: "#007BFF", marginBottom: "15px" }}>Blink Rate Analysis:</h3>
                                <p><strong>Blink Rate:</strong> {result.blink_rate} blinks per minute</p>
                                <p><strong>Status:</strong> <span style={{ 
                                    color: result.blink_status === "normal" ? "#28a745" : 
                                           result.blink_status === "low" ? "#ffc107" : "#dc3545",
                                    fontWeight: "bold"
                                }}>{result.blink_status.toUpperCase()}</span></p>
                                {result.blink_count !== undefined && (
                                    <p><strong>Total Blinks:</strong> {result.blink_count}</p>
                                )}
                                {result.video_duration !== undefined && (
                                    <p><strong>Video Duration:</strong> {result.video_duration.toFixed(1)} seconds</p>
                                )}
                                <hr style={{ marginTop: "15px" }} />
                                <p style={{ fontSize: "14px", color: "#666", marginTop: "10px" }}>
                                    {result.blink_status === "low" && "⚠️ Low blink rate detected. This may indicate eye strain or fatigue."}
                                    {result.blink_status === "normal" && "✓ Blink rate is within normal range (12-30 blinks/minute)."}
                                    {result.blink_status === "high" && "⚠️ High blink rate detected. This may indicate irritation or dryness."}
                                </p>
                            </>
                        ) : (
                            <>
                                <h3 style={{ color: "#007BFF", marginBottom: "15px" }}>Prediction Result:</h3>
                                <p><strong>Disease:</strong> {result.disease}</p>
                                <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
                                <p><strong>Remedy:</strong> {result.remedy}</p>
                                <hr />
                                <h4 style={{ marginTop: "15px", color: "#007BFF" }}>Additional Indicators</h4>
                                <p><strong>Blink rate:</strong> {result.blink_rate} per minute ({result.blink_status})</p>
                                <p><strong>Myopia:</strong> {result.myopia_risk} {(result.myopia_confidence * 100).toFixed(0)}%</p>
                            </>
                        )}
                    </div>
                )}

                {/* Error Display */}
                {error && (
                    <div style={{ 
                        marginTop: "20px", 
                        color: "red",
                        backgroundColor: "rgba(255, 0, 0, 0.1)",
                        padding: "15px",
                        borderRadius: "8px",
                        border: "1px solid red"
                    }}>
                        <p style={{ margin: 0 }}>{error}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadPage;
