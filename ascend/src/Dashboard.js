import './App.css';
import React, { useEffect, useState } from 'react';
import NavBar from './Components/Navbar';
import BottomBanner from './Components/BottomBanner';
import sidePencilImg from './Assets/Home/logo stretch.png';

function ContractHighlights() {
  return <div className="ContractHighlights">
    {/* TODO: get data from S3 */}
    <h1>UX Writer and Content Designer</h1>
    <button>Edit</button>
    <h2>Boa Constrictor & Company</h2>

    <div className="AnnualSalary">
      <h1>$96k</h1>
      <h2>annual salary</h2>
      <p><span className="lowlight">9% lower salary</span> than average</p>
      <p><span className="highlight">210% higher sign-on bonus</span> than average</p>
      <p><span className="lowlight">car insurance not included</span></p>
    </div>
  </div>;
}

const AnalyticsGraphs = () => {
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    // TODO: don't hardcode endpoint
    fetch('http://127.0.0.1:5001/get_salary_plot?location=CA&occupation=Data%20Scientists&contract=50')  
      .then((response) => response.blob()) 
      .then((blob) => {
        const url = URL.createObjectURL(blob); 
        setImageUrl(url); 
      })
      .catch((error) => console.error('Error fetching the image:', error));
  }, []); 

  return (
    <div className="AnalyticsGraphs">
      {/* <h1>Graphs:</h1> */}
      {imageUrl ? (
        <img src={imageUrl} alt="Graph" />
      ) : (
        <p>Loading...</p> 
      )}
    </div>
  );
};

function DashboardPage() {
  return (
    <div className="App">
      <NavBar />
      <ContractHighlights />
      <AnalyticsGraphs />
      <BottomBanner />
    </div>
  );
}

export default DashboardPage;
