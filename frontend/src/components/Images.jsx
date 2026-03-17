import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Image from 'react-bootstrap/Image';
import Row from 'react-bootstrap/Row';
import goatImg from "../Images/Goat.png";
import koalaImg from "../Images/Koala.png";
import squirrelImg from "../Images/Squirrel.png";

function Images() {
  //Creating three images next to each other for website decoration
  return (
    <div style={{
        display: "flex",
        justifyContent: "center",
        flexWrap: "wrap",
        gap: "20px"
    }}>
      <Image width="230" src={goatImg} rounded />
      <Image width="270" src={koalaImg} rounded />
      <Image width="180" src={squirrelImg} rounded />
    </div>
  );
}

export default Images;