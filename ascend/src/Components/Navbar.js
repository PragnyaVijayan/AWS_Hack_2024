import '../App.css';
import logo from '../Assets/Logo.png';

const NavBar = () => {
  return <div className="Bar">
    <img className="NavbarLogo" src={logo} alt="logo" />
    <a href="/dashboard" className="NavbarItem">Dashboard</a>
    <a href="/enterinfo" className="NavbarItem">New</a>
    <a href="/" className="NavbarItem">About</a>
    <a href="https://mail.google.com/mail/u/6/#inbox" target="_blank" className="NavbarItem messagesBtn">messages
      <div className="MessagesIcon">1</div>
    </a>
  </div>;
}

export default NavBar;