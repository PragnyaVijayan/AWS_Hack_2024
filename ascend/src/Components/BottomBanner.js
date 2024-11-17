import '../App.css';
import pencilImg2 from '../Assets/Home/PencilLogo.png'

const BottomBanner = () => {
  return (
    <div className="BottomBanner">
      <h1>Ascend</h1>
      <img src={pencilImg2}></img>
      <div className="namesCopyright">
        <p>Pragnya Vijayan </p>
        <p>Tiffany Nguyen </p>
        <p>Lydia Martin </p>
        <p>Lindsey Leong </p>
        <p>Maddie Follosco </p>
        <p>Irene Chang </p>
      </div>
    </div>
  );
}

export default BottomBanner;