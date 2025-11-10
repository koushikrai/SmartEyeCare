'use client'
import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import Link from 'next/link';

const MyNavbar = () => {
    return (
        <Navbar bg="dark" variant="dark" expand="lg">
            <Container>
                <Navbar.Brand as={Link} href="/">Smart Eye Care Portal</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} href="/">Home</Nav.Link>
                        <Nav.Link as={Link} href="/about">About Us</Nav.Link>
                        <Nav.Link as={Link} href="/upload">Predict</Nav.Link>
                        <Nav.Link as={Link} href="/prevent-measures">Preventive Measures</Nav.Link>
                        <Nav.Link as={Link} href="/feedback">Feedback</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default MyNavbar;
