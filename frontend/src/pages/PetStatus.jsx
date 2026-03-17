import goatImg from "../Images/Goat.png";
import { useEffect, useState } from "react";
import koalaImg from "../Images/Koala.png";
import squirrelImg from "../Images/Squirrel.png";
import { useLocation } from "react-router-dom";
import NavBar from "../components/NavBar";

function PetStatus() {
  // Retrieve pet_id, pet_type, and pet_name from navigation state
  const location = useLocation();
  const { pet_id, pet_type, pet_name } = location.state || {};
  // State to hold the pet's properties fetched from backend
  const [petsProperties, setPetsProperties] = useState(null);
  // Fetch pet properties on component mount or when pet_id changes
  useEffect(() => {
    if (!pet_id) return;
    const fetchData = async () => {
      try {
        const res = await fetch(
          `http://localhost:5000/pet_properties/${pet_id}`
        );
        const json = await res.json();
        setPetsProperties(json);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, [pet_id]);

  // Render nothing until properties are fetched
  if (!petsProperties) {
    return null;
  }

  // Map pet types to images
  const petTypeImages = {
    goat: goatImg,
    koala: koalaImg,
    squirrel: squirrelImg,
  };

  const typeKey = pet_type?.toLowerCase();
  const imgSrc = petTypeImages[typeKey];

  return (
    <>
      <NavBar />
      <img
        src={imgSrc || "/default-pet.png"}
        alt={pet_type}
        style={{
          position: "fixed",
          left: "10px",
          top: "140px",
          width: "580px",
          height: "auto",
        }}
      />
      <h1>Pet Name: {pet_name}</h1>
      <h1>Pet Type: {pet_type}</h1>
      <h1>Points: {petsProperties.points}</h1>
      <h1>
        Action History: {petsProperties.actions.join(", ")}
      </h1>
      <h1>Overall score: {petsProperties.overall_score}</h1>
    </>
  );
}

export default PetStatus;