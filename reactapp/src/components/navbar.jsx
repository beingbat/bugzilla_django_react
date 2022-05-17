import React from "react";
import "./navbar.css";
import {
  Container,
  Row,
  Col,
  Navbar,
  NavbarBrand,
  Nav,
  NavLink,
} from "reactstrap";

const Navigation = () => {
  return (
    <Navbar className="color-nav" sticky="top">
      <NavbarBrand className="mx-3 pt-2" href="/">
        <Container className="">
          <Row className="">
            <Col>
              <p className="display-7 white">
                React
                <br />
                App
              </p>
            </Col>
            <Col className="">
              <p className="display-6 mt-2 white">BUGZILLA</p>
            </Col>
          </Row>
        </Container>
      </NavbarBrand>

      <Nav className="pb-2 mr-auto">
        <NavLink className="white" href="/">
          DASHBOARD
        </NavLink>
        <NavLink className="white" href="/accounts/logout">
          LOGOUT
        </NavLink>
      </Nav>
    </Navbar>
  );
};

export default Navigation;
