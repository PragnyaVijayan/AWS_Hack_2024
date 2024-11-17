import './App.css';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

import NavBar from './Components/Navbar';
import BottomBanner from './Components/BottomBanner';

function ContractHighlights() {
  const navigate = useNavigate();

  // Get Data from S3
  const [userData, setUserData] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/s3_user_read");
      setUserData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      // alert("Failed to fetch data.");
    }
  };

  // UseEffect to call fetchData when the component mounts
  useEffect(() => {
    fetchData();
  }, []);

  return <div className="ContractHighlights">    
    <h1>{userData?userData["jobInputVal"]:"UX Writer and Content Designer"}</h1>
    <button onClick={() => navigate('/enterinfo')}>Edit</button>
    <h2>{userData?userData["skillInputVal"] : "Boa Constrictor & Company"}</h2>

    <div className="AnnualSalary">
      <div className="AnnualSalaryPopup">
        <h4 className="AnnualSalaryPopupLeft">paid leave and dental medical covered</h4>
        <div>
          <h1>$96k</h1>
          <h2>annual salary</h2>
        </div>
        <div className="AnnualSalaryPopupRight">
        <h3>$32k</h3>
        <h4>sign-on bonus</h4>
        </div>
      </div>
      <p><span className="lowlight">9% lower salary</span> than average</p>
      <p><span className="highlight">210% higher sign-on bonus</span> than average</p>
      <p><span className="lowlight">car insurance not included</span></p>
    </div>
  </div>;
}

const AnalyticsGraphs = () => {
  // Get user data
  const [userData, setUserData] = useState(null);

  // Get User input data
  const getUserData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/s3_user_read");
      setUserData(response.data);
    } catch (error) {
      // console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    getUserData();
  }, []);

  // Get percentile graph for the user's job
  const [salaryPercentileImgUrl, setSalaryPercentileImgUrl] = useState(null);
  const [salaryTrendImgUrl, setSalaryTrendImgUrl] = useState(null);

  const fetchPercentileData = async () => {
    // TODO: don't hardcode contract
    // Get Salary Percentile from API
    fetch(`http://127.0.0.1:5001/get_salary_plot?location=${userData? userData.stateInputVal : ""}&occupation=${userData? userData.jobInputVal : "Data%20Scientists"}&contract=50`)
      .then((response) => response.blob()) 
      .then((blob) => {
        const url = URL.createObjectURL(blob); 
        setSalaryPercentileImgUrl(url); 
      })
      .catch((error) => alert('Error fetching the graph:', error));
  };

  useEffect(() => {
    fetchPercentileData();
  }, [userData]);

  // Get user's inputed salary trend graph
  useEffect(() => {
    fetch('http://127.0.0.1:5001/job_salary_trend?contract=50')  
    .then((response) => response.blob()) 
    .then((blob) => {
      const url = URL.createObjectURL(blob); 
      setSalaryTrendImgUrl(url); 
    })
    .catch((error) => console.error('Error fetching the image:', error));
  }, []); 

  return (
    <div className="AnalyticsGraphs">
      {/* <h1>Graphs:</h1> */}
      {salaryPercentileImgUrl ? (
        <img src={salaryPercentileImgUrl} alt="Graph" />
      ) : (
        <p>Loading...</p> 
      )}
      {salaryTrendImgUrl ? (
        <img src={salaryTrendImgUrl} alt="Graph" />
      ) : (
        <p>Loading...</p> 
      )}
    </div>
  );
};

function ContractMainPoints() {
  const [points, setPoints] = useState([]);

  // Convert the text to an array of sentences
  function convertToList(text) {
    const sentences = text.split('.').map(sentence => sentence.trim()).filter(Boolean);
    return sentences;
  }

  // Fetch the contract summary
  const fetchContractSummary = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5003/read_contract_summary');
      const data = await response.json(); // Parse the response body as JSON

      // Parse summary data
      const servicesList = convertToList(data.services);
      const milestonesList = convertToList(data.milestones);

      // Merge the two lists and set the points state
      setPoints([...servicesList, ...milestonesList]); // Using spread operator to combine both arrays
    } catch (error) {
      alert('Error fetching summary:', error);
    }
  };

  // Fetch contract summary when the component is mounted
  useEffect(() => {
    fetchContractSummary();
  }, []);

  return (
    <div className="ContractMainPoints">
      <h1>Contract Verdict:</h1>
      <h1>not good</h1>
      <div className="Points">
        <ul>
          {points.map((curPoint, index) => (
            <li key={index}>{curPoint}</li> // Use key for each list item
          ))}
        </ul>
      </div>
    </div>
  );
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
