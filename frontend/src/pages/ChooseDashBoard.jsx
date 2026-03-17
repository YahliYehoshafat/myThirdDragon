import '../App.css';
import './ChooseDashBoard.css'
import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import { useNavigate } from 'react-router-dom';
import goatImg from "../Images/Goat.png";
import koalaImg from "../Images/Koala.png";
import squirrelImg from "../Images/Squirrel.png";

function ChooseDashBoard() {
  // State to hold the user's pets
  const [pets, setPets] = useState([]);
  const navigate = useNavigate();

  // Mapping pet types to images
  const petTypeImages = {
    goat: goatImg,
    koala: koalaImg,
    squirrel: squirrelImg,
  };

  // Fetch pet info on component mount
  useEffect(() => {
    fetch("http://localhost:5000/pet_info")
      .then(response => response.json())
      .then(data => setPets(data))
      .catch(err => console.error(err));
  }, []);

  const goToDashboard = (pet_id) => {
    navigate('/DashBoard', { state: { pet_id } });
  };

  return (
    <>
      <NavBar />

      <h1 className="dashboard-title">
        Choose the pet you would like to view
      </h1>

      {pets.length === 0 && (
        <p className="no-pets-message">
          You don't have any pets right now :( Create your own pet :)
        </p>
      )}

      <div className="dashboard-container">
        {pets.map((pet) => {
          const typeKey = pet.pet_type.toLowerCase();
          const imgSrc = petTypeImages[typeKey];

          return (
            <div
              key={pet.pet_id}
              className="pet-card"
              onClick={() => goToDashboard(pet.pet_id)}
            >
              <img
                src={imgSrc || "/default-pet.png"}
                alt={pet.name}
                className="pet-image"
              />

              <h3 className="pet-name">
                {pet.name || pet.pet_name}
              </h3>
            </div>
          );
        })}
      </div>
    </>
  );
}

export default ChooseDashBoard;