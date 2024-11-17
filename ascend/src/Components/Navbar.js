import '../App.css';
import logo from '../Assets/Logo.png';

const NavBar = () => {
  return <div className="Bar">
    <img className="NavbarLogo" src={logo} alt="logo" />
    <a href="/dashboard" className="NavbarItem">Dashboard</a>
    <a href="/enterinfo" className="NavbarItem">New</a>
    <a href="/" className="NavbarItem">About</a>
  </div>;
}

export default NavBar;