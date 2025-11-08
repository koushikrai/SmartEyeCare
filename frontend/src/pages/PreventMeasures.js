import React from "react";
import { Container, Row, Col, Card, Carousel } from "react-bootstrap";

const PreventiveMeasure = () => {

    const backgroundStyle = {
        backgroundColor: "#b7d7e8",
        minHeight: "100vh",
        padding: "20px",
        filter: "brightness(85%)",
    };

    // Example news/awareness carousel
    const news = [
        {
            title: "Rise in Digital Eye Strain in Kids",
            description: "Pediatricians warn of increasing screen-related vision problems among children.",
            img: "https://www.idahofallsmagazine.com/Images/Articles/1676/eye%20series-5.JPG_1600.jpg"
        },
        {
            title: "Blue Light Exposure and Sleep Disruption",
            description: "Limiting screen time before bed can improve eye health and sleep quality in kids.",
            img: "https://images.squarespace-cdn.com/content/v1/5cb5b1e2049079446d948bf9/b2a77900-b1a3-4aeb-800c-e3dddd0aa0cb/The+effects+of+blue+light+on+your+child%E2%80%99s+health+and+sleep..png?format=2500w"
        },
        {
            title: "WHO Guidelines on Screen Time for Children",
            description: "Children under 5 should not exceed 1 hour of screen time per day.",
            img: "https://cdn.shopify.com/s/files/1/0550/4670/1130/files/screentime-V2.png?v=1654290545"
        }
    ];

    // Common symptoms and preventive actions
    const tips = [
        {
            name: "Dry or Irritated Eyes",
            prevention: "Encourage kids to blink more often and use artificial tears if needed. Ensure they take breaks every 20 minutes."
        },
        {
            name: "Eye Redness or Fatigue",
            prevention: "Maintain proper screen distance (at least 18–24 inches) and reduce ambient glare with soft lighting."
        },
        {
            name: "Headaches or Blurred Vision",
            prevention: "Use blue light filters on devices, and limit continuous screen exposure to no more than 30 minutes."
        },
        {
            name: "Poor Posture and Eye Strain",
            prevention: "Ensure ergonomic seating and monitor height. Use the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds."
        },
    ];

    return (
        <div style={backgroundStyle}>
            <Container className="mt-5">
                {/* Carousel Section */}
                <Row className="justify-content-center mb-5">
                    <Col md={8}>
                        <Carousel>
                            {news.map((item, index) => (
                                <Carousel.Item key={index}>
                                    <img
                                        className="d-block w-100"
                                        src={item.img}
                                        alt={item.title}
                                        style={{ height: "400px", objectFit: "cover" }}
                                    />
                                    <Carousel.Caption>
                                        <h3>{item.title}</h3>
                                        <p>{item.description}</p>
                                    </Carousel.Caption>
                                </Carousel.Item>
                            ))}
                        </Carousel>
                    </Col>
                </Row>

                {/* Preventive Tips Section */}
                <Row>
                    <Col>
                        <h2 className="text-center mb-4">Common Eye Strain Symptoms and Preventive Measures</h2>
                        {tips.map((tip, index) => (
                            <Card className="mb-3" key={index}>
                                <Card.Body>
                                    <Card.Title>{tip.name}</Card.Title>
                                    <Card.Text>
                                        <strong>Prevention:</strong> {tip.prevention}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                        ))}
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default PreventiveMeasure;
