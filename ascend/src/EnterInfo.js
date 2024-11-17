import './App.css';
import NavBar from './Components/Navbar';
import BottomBanner from './Components/BottomBanner';
import sidePencilImg from './Assets/Home/logo stretch.png';

function EnterInfo() {
  return <div className="EnterInfo">
    <h1>Fill in the <span className="blankText">blank.</span></h1>
    <h2>For work, I am a </h2>
    <input name="myInput" className="userInput jobInput" />
    <h2>.</h2>
    
    <br></br>
    <h2>I have </h2>
    <input name="myInput" className="userInput yearsInput" />
    <h2> years of experience.</h2>

    <br></br>
    <h2>I currently work with </h2>
    <input name="myInput" className="userInput skillInput" />
    <h2>.</h2>

    <br></br>
    <h2>My desired salary is </h2>
    <input name="myInput" className="userInput salaryInput" />
    <h2>.</h2>
  </div>;
}

function EnterInfoPage() {
  return (
    <div className="App">
      <NavBar />
      <EnterInfo />
      <BottomBanner />
    </div>
  );
}

export default EnterInfoPage;
