import '../App.css'
import NavBar from '../components/NavBar'
import Images from '../components/Images'

function Home() {
  //Home page
  return (
    <>
      <NavBar/>
      <h1 fixed="top" style={{marginBottom: "200px", fontSize: "70px"}}>Your pet is waiting for you!</h1>
      <Images/>
    </>
  )
}

export default Home
