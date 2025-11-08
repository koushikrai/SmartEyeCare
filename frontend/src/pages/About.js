import React from "react";
import { Container, Row, Col, Card, Carousel } from "react-bootstrap";

const About = () => {
    const backgroundStyle = {
        backgroundColor: "#3c5461ff",
        minHeight: "100vh",
        padding: "20px",
        filter: "brightness(85%)",
    };

    const carouselImageStyle = {
        filter: "brightness(90%) contrast(90%)",
        height: "400px",
        objectFit: "cover",
    };

    return (
        <div style={backgroundStyle}>
            <Container className="mt-5">
                {/* Carousel Section */}
                <Row className="justify-content-center mb-5">
                    <Col md={8}>
                        <Carousel>
                            <Carousel.Item>
                                <img
                                    className="d-block w-100"
                                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKwQ9M7PAwtDD5_M1GczCD38qQnkGBft_LOw&s"
                                    alt="First slide"
                                    style={carouselImageStyle}
                                />
                                <Carousel.Caption>
                                    <h3>AI for Vision Health</h3>
                                    <p>
                                        Monitor and protect children's eye health in real-time using advanced AI and computer vision.
                                    </p>
                                </Carousel.Caption>
                            </Carousel.Item>
                            <Carousel.Item>
                                <img
                                    className="d-block w-100"
                                    src="https://myeyewellness.com/wp-content/uploads/2022/11/Can-Screen-Time-Cause-Dry-Eyes_-Hero.jpeg"
                                    alt="Second slide"
                                    style={carouselImageStyle}
                                />
                                <Carousel.Caption>
                                    <h3>Prevent Screen-Induced Eye Strain</h3>
                                    <p>
                                        Detect early signs of digital eye strain based on blink patterns and redness level.
                                    </p>
                                </Carousel.Caption>
                            </Carousel.Item>
                            <Carousel.Item>
                                <img
                                    className="d-block w-100"
                                    src="https://shaheyecenter.com/wp-content/uploads/pediatric-eyecare-1-1024x683.jpg"
                                    alt="Third slide"
                                    style={carouselImageStyle}
                                />
                                <Carousel.Caption>
                                    <h3>Smart Care for Kids' Eyes</h3>
                                    <p>
                                        AI-powered insights to promote healthier screen habits for children aged 3–12.
                                    </p>
                                </Carousel.Caption>
                            </Carousel.Item>
                        </Carousel>
                    </Col>
                </Row>

                {/* About Section */}
                <Row className="justify-content-center">
                    <Col md={8}>
                        <Card>
                            <Card.Body>
                                <Card.Title className="text-center mb-4">
                                    About Smart Eye Care
                                </Card.Title>
                                <Card.Text>
                                    The <strong>Smart Eye Care Portal</strong> is an AI-based health monitoring system designed to analyze and predict eye strain in children aged 3–12, caused by prolonged screen exposure.
                                </Card.Text>
                                <Card.Text>
                                    By using computer vision techniques such as blink detection and redness analysis, along with a trained deep learning model, this system helps in:
                                </Card.Text>
                                <ul>
                                    <li>Real-time monitoring of eye strain and fatigue levels.</li>
                                    <li>Early detection of harmful screen time effects.</li>
                                    <li>Providing actionable insights for healthier digital habits.</li>
                                </ul>
                                <Card.Text>
                                    The portal is especially useful for parents, educators, and pediatricians to track visual health and take preventive steps before chronic issues develop.
                                </Card.Text>
                                <Card.Text className="text-center mt-4">
                                    <strong>Together, let's build a safer digital environment for children’s vision health!</strong>
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default About;
