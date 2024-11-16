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

function App() {
  return (
    <div className="App">
      <NavBar />
      <Header />
    </div>
  );
}

export default App;

