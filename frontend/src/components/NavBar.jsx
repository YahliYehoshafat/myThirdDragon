import Container from 'react-bootstrap/Container';
import { Link } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import "./NavBar.css";

function NavBar() {
  //A nav bar that allows navigation between pages on the website.
  return (
    <Navbar expand="lg" className="NavBar rounded w-100" fixed="top" >
      <Container fluid>
        <Navbar.Brand as={Link} to="/">Pets App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/Home">Home</Nav.Link>
            <Nav.Link as={Link} to="/PetInfo">Pet Info</Nav.Link>
            <Nav.Link as={Link} to="/CreateANewPet">Create A New Pet</Nav.Link>
            <Nav.Link as={Link} to="/ChooseDashBoard">Choose Dash Board</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;