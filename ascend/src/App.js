// import React.
import './App.css';
import logo from './Assets/Logo.png';
import paperImg from './Assets/Home/paper graphics.png';
import pencilImg from './Assets/Home/sharp ver.png';


// class navBar extends React.Component {
//   render(){
//     return <div className="Bar"></div>
//   };
// }

function NavBar() {
  return <div className="Bar">
    <img className="NavbarLogo" src={logo} />
    <a className="NavbarItem">Dashboard</a>
    <a className="NavbarItem">New</a>
    <a className="NavbarItem">About</a>
  </div>;
}

function Header() {
  return <div className="Header">
    <img className="PencilImg" src={pencilImg} />
    <img className="PaperImg" src={paperImg} />
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


function App() {
  return (
    <div className="App">
      <NavBar />
      <Header />
      <WhatsAscend />
    </div>
  );
}

export default App;

