'use client'
import React, { useState, useRef } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import "./UploadPage.css";

const UploadPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [useWebcam, setUseWebcam] = useState(false);
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

    const captureImageFromWebcam = () => {
        const imageSrc = webcamRef.current.getScreenshot();
        return fetch(imageSrc)
            .then(res => res.blob())
            .then(blob => new File([blob], "captured_eye.jpg", { type: "image/jpeg" }));
    };

    const handleUpload = async () => {
        setIsLoading(true);
        setError(null);

        try {
            let fileToUpload = selectedFile;

            // If webcam mode is on, capture image
            if (useWebcam) {
                fileToUpload = await captureImageFromWebcam();
            }

            if (!fileToUpload) {
                setError("No image provided. Please upload or capture an eye image.");
                setIsLoading(false);
                return;
            }

            const formData = new FormData();
            formData.append("image", fileToUpload);

            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            setResult(response.data);
        } catch (err) {
            console.error("Upload failed:", err);
            setError("Failed to upload image or get prediction.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <div style={{ padding: "20px", textAlign: "center", fontFamily: "Arial, sans-serif" }}>
                <h1 style={{ fontSize: "50px", color: "#007BFF" }}>Smart Eye Health Check</h1>
                <p style={{ marginBottom: "20px", fontSize: "20px", color: "orange" }}>
                    Upload or scan an eye to detect signs of strain, redness, or myopia.
                </p>

                {/* Toggle between upload and webcam */}
                <div style={{ marginBottom: "10px", display: "flex", justifyContent: "center", gap: "10px" }}>
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

                {/* Conditional Input */}
                {!useWebcam ? (
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileChange}
                        style={{ marginBottom: "15px" }}
                    />
                ) : (
                    <div style={{ display: "flex", justifyContent: "center", marginBottom: "15px" }}>
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
                    style={{
                        padding: "10px 20px",
                        cursor: "pointer",
                        backgroundColor: "#28a745",
                        color: "white",
                        border: "none",
                        borderRadius: "15px",
                        width: "220px",
                        marginBottom: "30px"
                    }}
                >
                    {isLoading ? "Processing..." : useWebcam ? "Capture & Predict" : "Upload & Predict"}
                </button>

                {/* Result Section */}
                <div style={{border:"2px solid black",marginTop:"40px",backgroundColor:"white",filter:"contrast(80%)"}}>
            {result && (
                <div style={{ marginTop: "20px", textAlign: "left", maxWidth: "500px", margin: "0 auto" ,color:"black"}}>
                    <h3>Prediction Result:</h3>
                    <p><strong>Disease:</strong> {result.disease}</p>
                    <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
                    <p><strong>Remedy:</strong> {result.remedy}</p>
                </div>
               
                    )}
                </div>

                {/* Error Display */}
                {error && (
                    <div style={{ marginTop: "20px", color: "red" }}>
                        <p>{error}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadPage;
