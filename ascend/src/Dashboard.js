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

function ContractMainPoints() {
  // TODO: get actual points
  const points = ["5 years of work guaranteed", "NDA required", "Covers both family dental and health insurance.",
    "Required relocation to Antarctica", "The soul of your first newborn son required", "Not responsible for death, injury, or illness"];
  
  return <div className="ContractMainPoints">
    <h1>Contract Verdict:</h1>
    <h1>not good</h1>
    <div className="Points">
      <ul>
        {points.map((curPoint, index) => (
          <li key={index}>{curPoint}</li> // Use key for each list item
        ))}
      </ul>
    </div>
  </div>;
}

function NegotiationPoints() {
  // TODO: get actual points
  const values = [
    ["Required relocation to Antarctica", "You live in Argentina. The commute to Antarctica is only 1.4 hours. Perhaps you could bring up the possibility of commuting?"],
    ["9% lower salary on average", "UX Writers and Content Designers with 3 years of experience get paid $105k on average."],
    ["The soul of your firstborn son required", "UX Writers and Content Designers are usually not required to give up the soul of their firstborn son. Maybe you can bring up your awesome Excel skills?"]
  ];

  return (
    <div className="NegotiationPointsContainer">
      <h1>Negotiation Points:</h1>
      <div className="NegotiationPoints">
      {values.flat().map((item, index) => (
        <div className="grid-item" key={index}>
          {item}
        </div>
      ))}
      </div>
    </div>
  );
}

function DashboardPage() {
  return (
    <div className="App">
      <NavBar />
      <ContractHighlights />
      <AnalyticsGraphs />
      <ContractMainPoints />
      <NegotiationPoints />
      <BottomBanner />
    </div>
  );
}

export default DashboardPage;
