import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import CreateANewPet from './pages/CreateANewPet';
import PetInfo from './pages/PetInfo';
import PetProperties from './pages/PetProperties';
import DashBoard from './pages/DashBoard';
import LoginSignup from './pages/LoginSignup';
import PetStatus from './pages/PetStatus';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import ChooseDashBoard from "./pages/ChooseDashBoard";

function App() {
  //The main file, where the routes between the pages are defined.
  return (
    <BrowserRouter>
      <Routes>  
        <Route path="/" element={<LoginSignup />} /> 
        <Route path="/Home" element={<Home />} /> 
        <Route path="/PetInfo" element={<PetInfo />} /> 
        <Route path="/CreateANewPet" element={<CreateANewPet />} /> 
        <Route path="/PetProperties" element={<PetProperties />} /> 
        <Route path="/PetStatus" element={<PetStatus />} /> 
        <Route path="/ChooseDashBoard" element={<ChooseDashBoard />} /> 
        <Route path="/DashBoard" element={<DashBoard />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;