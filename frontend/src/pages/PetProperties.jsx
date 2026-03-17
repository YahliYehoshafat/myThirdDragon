import Image from 'react-bootstrap/Image';
import goatImg from "../Images/Goat.png";
import { useLocation } from "react-router-dom";
import MyProgressBar from "../components/MyProgressBar"
import NavBar from "../components/NavBar";
import { useEffect, useState } from "react";
import koalaImg from "../Images/Koala.png";
import squirrelImg from "../Images/Squirrel.png";

function PetProperties() {
  //Pet properties page, here you receive important information about the pet, and in addition, you can perform actions with your pet!
  const location = useLocation();
  const [pet, setPet] = useState(null);
  const petTypeImages = {
    goat: goatImg,
    koala: koalaImg,
    squirrel: squirrelImg,
  };

  //Information about the pet, received from the PetInfo file.
  const { pet_id, pet_type, name } = location.state || {};
  const [petsProperties, setPetsProperties] = useState([]);
  const [progress, setProgress] = useState([0, 0, 0]);

  useEffect(() => {
    if (!pet_id) return;
    const fetchData = async () => {
      try {
        const res = await fetch(`http://localhost:5000/pet_properties/${pet_id}`);
        const json = await res.json();
        setProgress([json.hunger, json.happiness, json.energy]);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [pet_id]);
  
  console.log("progress = " + progress)
  console.log("happiness = " + petsProperties.happiness)
  const typeKey = pet_type.toLowerCase(); 
  const imgSrc = petTypeImages[typeKey];
  //Access the endpoint on the server responsible for performing actions like sleeping, playing, and eating in order to take care of the pet.
  const handleSubmit = async (pet_id, action) => {
    try {
      const response = await fetch(`http://localhost:5000/performing_an_action`, {
        method: 'POST',               
        headers: {
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify({       
          pet_id: pet_id,
          action: action
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPet(data); 
      setProgress([data.hunger, data.happiness, data.energy]);
      
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <>
        <NavBar/>
        <Image 
          style={{ 
              position: "fixed",  
              left: "10px",          
              top: "140px",      
              width: "580px",
              height: "auto",
          }} 
          src={imgSrc} alt={name}
          rounded 
        />

        <div style={{ display: "flex", alignItems: "center", gap: "20px"}}>
          <MyProgressBar value={progress[0]} label="Hunger"/>
          <button
            style={{
              padding: "10px 20px",
              marginLeft: "50px",
              fontSize: "16px",
              cursor: "pointer"
            }} onClick={() => handleSubmit(pet_id, "eat")}
          >
            Eat
          </button>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "20px"}}>
          <MyProgressBar value={progress[1]} label="Happiness"/>
          <button
            style={{
              padding: "10px 20px",
              marginLeft: "50px",
              fontSize: "16px",
              cursor: "pointer"
            }} onClick={() => handleSubmit(pet_id, "play")}
          >
            Play
          </button>
        </div>
        
        <div style={{ display: "flex", alignItems: "center", gap: "20px"}}>
          <MyProgressBar value={progress[2]} label="Energy"/>
          <button
            style={{
              padding: "10px 20px",
              marginLeft: "50px",
              fontSize: "16px",
              cursor: "pointer"
            }} onClick={() => handleSubmit(pet_id, "sleep")}
          >
            Sleep
          </button>
        </div>
    </>
  );
}

export default PetProperties;