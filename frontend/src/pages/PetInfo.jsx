import '../App.css';
import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import { useNavigate } from 'react-router-dom';
import goatImg from "../Images/Goat.png";
import koalaImg from "../Images/Koala.png";
import squirrelImg from "../Images/Squirrel.png";

function PetInfo() {
  // State to hold all pets
  const [pets, setPets] = useState([]);
  // State to hold the currently selected pet
  const [selectedPet, setSelectedPet] = useState(null); 
  const navigate = useNavigate();

  // Handles selecting a pet from the list
  const handleSelect = (pet) => {
    setSelectedPet(pet);
  };

  // Navigate to PetProperties page for the selected pet
  const PetProperties = () => {
    if (selectedPet) {
      navigate('/PetProperties', 
        {state: {
          pet_id: selectedPet.pet_id,
          pet_type: selectedPet.pet_type, 
          pet_name: selectedPet.pet_name, 
        }});
    } 
  };

  // Navigate to PetStatus page for the selected pet
  const PetStatus = () => {
    if (selectedPet) {
      navigate('/PetStatus', 
        {state: {
          pet_id: selectedPet.pet_id,
          pet_type: selectedPet.pet_type, 
          pet_name: selectedPet.pet_name, 
        }});
    } 
  };

  // Map pet types to images
  const petTypeImages = {
    goat: goatImg,
    koala: koalaImg,
    squirrel: squirrelImg,
  };

  // Fetch pets from backend on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:5000/pet_info");
        const json = await res.json();
        setPets(json);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, []);

  console.log("pets = " + pets)

  return (
    <>
      <NavBar/>
      {pets.length === 0 && <p>You don't have any pets right now :( Create your own pet :)</p>}

      <div style={{ display: "flex", flexWrap: "wrap", gap: "30px" }}>
        {pets.map((pet, index) => {
          console.log("pet type = " + pet.pet_type)
          const typeKey = pet.pet_type.toLowerCase(); 
          const imgSrc = petTypeImages[typeKey];

          const isSelected = selectedPet === pet;

          return (
            <div
                key={index} 
                onClick={() => handleSelect(pet, index)}
                style={{
                  cursor: "pointer",
                  width: "auto",
                  textAlign: "center",
                  border: isSelected ? "4px solid #007bff" : "2px solid #ccc",
                  borderRadius: "12px",
                  padding: "4px",
                  transition: "all 0.2s",
                }}
              >
                <img
                  src={imgSrc || "/default-pet.png"}
                  alt={pet.pet_name} 
                  style={{
                    width: "100%",
                    height: "190px",
                    objectFit: "cover",
                    borderRadius: "8px",
                    boxShadow: "0 2px 6px rgba(0,0,0,0.3)",
                  }}
                />
                <p style={{ marginTop: "8px", fontWeight: "bold" }}>{pet.pet_name}</p> 
              </div>
            );
          })}
      </div>

      <div style={{ marginTop: "20px" }}>
        <button 
          onClick={PetProperties} 
          style={{ padding: "10px 20px", marginRight: "100px", marginTop: "50px", fontSize: "16px", cursor: "pointer" }}
        >
          Pet Properties
        </button>

        <button 
          onClick={PetStatus} 
          style={{ padding: "10px 20px", marginLeft: "100px", marginTop: "50px", fontSize: "16px", cursor: "pointer" }}
        >
          Pet Status
        </button>
      </div>
    </>
  );
}

export default PetInfo;