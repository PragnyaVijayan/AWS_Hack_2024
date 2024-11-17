import '../App.css';
import logo from '../Assets/Logo.png';

const NavBar = () => {
  return <div className="Bar">
    <img className="NavbarLogo" src={logo} alt="logo" />
    <a className="NavbarItem">Dashboard</a>
    <a className="NavbarItem">New</a>
    <a className="NavbarItem">About</a>
  </div>;
}

export default NavBar;