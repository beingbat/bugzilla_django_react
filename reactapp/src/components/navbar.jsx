import React from "react";
import { Container, Row, Col, Navbar, NavbarBrand, Nav, NavLink } from "reactstrap";

const Navigation = () => {
  return (
    <Navbar bg="dark" variant="dark" sticky='top' >
      <NavbarBrand className="mx-3" href="#">
        <Container>
          <Row>
            <Col>
              <p className="display-7 mr_auto">
                React
                <br />
                App
              </p>
            </Col>
            <Col className="mr_auto">
              <p className="display-6 mr_auto">BUGZILLA</p>
            </Col>
          </Row>
        </Container>
      </NavbarBrand>

      <Nav>
        <NavLink href="/">DASHBOARD</NavLink>
        <NavLink href="/logout">LOGOUT</NavLink>
      </Nav>
    </Navbar>
  );
};

export default Navigation;
