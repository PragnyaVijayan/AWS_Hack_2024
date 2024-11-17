// import React.
import './App.css';
import logo from './Assets/Logo.png';
import paperImg from './Assets/Home/paper graphics.png';
import pencilImg from './Assets/Home/sharp ver.png';
import capyImg from './Assets/Home/capy.png';
import sidePencilImg from './Assets/Home/logo stretch.png'

function NavBar() {
  return <div className="Bar">
    <img className="NavbarLogo" src={logo} alt="logo" />
    <a className="NavbarItem">Dashboard</a>
    <a className="NavbarItem">New</a>
    <a className="NavbarItem">About</a>
  </div>;
}

function Header() {
  return <div className="Header">
    <img className="PencilImg" src={pencilImg} alt=""/>
    <img className="PaperImg" src={paperImg} alt =""/>
    <div className="HeaderText">
      <h1>Ascend</h1>
      <h2>fly high.</h2>
    </div>
  </div>;
}

function WhatsAscend(){
  return <div className="WhatsAscend">
    <div className="WhatsAscendBox">
      <h1>What's Ascend?</h1>
      <p>
      Ascend is an on-demand contract negotiator that makes it easy to get the conditions you deserve.
      <br></br>
      <br></br>
      Just enter a few characters and a copy of your contract. Try it now.
      </p>

      <button>Ascend</button>
    </div>
  </div>;
}

function Creators(){
  return <div className="Creators">
    <div className="CreatorsBox">
      <h1>Who made this?</h1>
      <div className = "CreatorsList">
        <CreatorCard 
          image={capyImg}
          name="Pragnya Vijayan"
          role="backend"
        />
        <CreatorCard 
          image={capyImg}
          name="Tiffany Nguyen"
          role="frontend/backend"
        />
        <CreatorCard 
          image={capyImg}
          name="Lydia Martin"
          role="backend"
        />
        <CreatorCard 
          image={capyImg}
          name="Lindsey Leong"
          role="design"
        />
        <CreatorCard 
          image={capyImg}
          name="Maddie Follosco"
          role="backend"
        />
        <CreatorCard 
          image={capyImg}
          name="Irene Chang"
          role="backend"
        />
      </div>
    </div>
  </div>;
}

function CreatorCard({ image, name, role }) {
  return (
    <div className="CreatorCard">
      <img src={image} alt=""/>
      <h1>{name}</h1>
      <h2>{role}</h2>
    </div>
  );
}

function SidePencil() {
  return (
    <img className="SidePencil" src={sidePencilImg} alt=""/>
  );
}

function App() {
  return (
    <div className="App">
      <NavBar />
      <Header />
      <WhatsAscend />
      <Creators />
      <SidePencil />
    </div>
  );
}

export default App;

