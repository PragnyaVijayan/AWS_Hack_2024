import './App.css';
import './Contract.css';

import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";

import NavBar from './Components/Navbar';
import BottomBanner from './Components/BottomBanner';
import sidePencilImg from './Assets/Home/logo stretch.png'
import upload from './imgs/upload.png';

function SidePencil() {
  return (
    <img className="SidePencil2" src={sidePencilImg} alt=""/>
  );
}

function EnterInfo() {
  const navigate = useNavigate();

  const [jobInputVal, setJobInputVal] = useState("");
  const [yearsInputVal, setYearsInputVal] = useState("");
  const [skillInputVal, setSkillInputVal] = useState("");
  const [salaryInputVal, setSalaryInputVal] = useState("");
  const [stateInputVal, setStateInputVal] = useState("");
  const [pastSalaryInputVal, setPastSalaryInputVal] = useState("");

  const handleSubmit = async () => {
    // Save data in S3
    const userInputData = {
      "jobInputVal": jobInputVal,
      "yearsInputVal": yearsInputVal,
      "skillInputVal": skillInputVal,
      "salaryInputVal": salaryInputVal,
      "stateInputVal": stateInputVal,
      "pastSalaryInputVal":pastSalaryInputVal,
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/s3_user_upload", userInputData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
    } catch (error) {
      console.error("Error uploading data:", error);
      alert("Failed to upload data.");
    }

    // Navigate to next page
    navigate('/dashboard')
  };

  return <div className="EnterInfo">
    <h1>Fill in the <span className="blankText">blank.</span></h1>
    <h2>For work, I am a </h2>
    <input type="text" value={jobInputVal} onChange={(event) => setJobInputVal(event.target.value)} name="myInput" className="userInput jobInput" />
    <h2>.</h2>
    
    <br></br>
    <h2>I have </h2>
    <input type="text" value={yearsInputVal} onChange={(event) => setYearsInputVal(event.target.value)} name="myInput" className="userInput yearsInput" />
    <h2> years of experience.</h2>

    <br></br>
    <h2>I am considering a position at </h2>
    <input type="text" value={skillInputVal} onChange={(event) => setSkillInputVal(event.target.value)} name="myInput" className="userInput skillInput" />
    <h2>.</h2>

    <br></br>
    <h2>My desired hourly salary is </h2>
    <input type="text" value={salaryInputVal} onChange={(event) => setSalaryInputVal(event.target.value)} name="myInput" className="userInput salaryInput" />
    <h2>.</h2>

    <br></br>
    <h2>The state I am located in is</h2>
    <input type="text" value={stateInputVal} onChange={(event) => setStateInputVal(event.target.value)} name="myInput" className="userInput stateInput" />
    <h2>.</h2>

    <br></br>
    <h2>My past hourly salaries have been</h2>
    <input type="text" value={pastSalaryInputVal} onChange={(event) => setPastSalaryInputVal(event.target.value)} name="myInput" className="userInput pastSalaryInput" />
    <h2>.</h2>

    <Contract />

    <button onClick={handleSubmit} className="ContinueBtn">Continue</button>
  </div>;
}



function Contract() {
  
  // State to store uploaded file
  const [selectedFile, setSelectedFile] = useState(null);
  const [summaries, setSummary] = useState("");

  // function controlChange(e) {
  //   setSelectedFile(URL.createObjectURL(e.target.files[0]));
  // }

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
  }

  const controlUpload = async () => {
    if(!selectedFile) {
      alert("Please select a file to upload");
      return;
    }

    const fd = new FormData();
    fd.append('file', selectedFile);

    try {
      const res = await axios.post("http://127.0.0.1:5000/summarize", fd, {
        headers: {
          'Content-Type': "multipart/form-data",
        },
      });
      setSummary(res.data.summaries);
    } catch(error) {
      console.error("Error", error);
      alert("An error occurred while uploading the file");
    }
  };

  return (
    <div className="App">
      <header className="contract-text">
        <h2>
          <p>Finally,</p>
          <p>upload your contract.</p>
        </h2>
      </header>
        <div className='contract-visual'>
          <img id = "upload_img" src={upload} alt="upload"/>
            <br/>
            <br/>
            <div className='file_upload_container'>
              <div className = 'file_upload_box'>
                <label htmlFor="file_input" className="file-input-text">
                  <b>Upload</b>
                </label>
                {/* (e) => {setSelectedFile(e.target.files[0]) }  */}
                <input type="file" id = "file_input" onChange={ handleFileChange } accept=".pdf" style={{ display: 'none' }}/>
                <br/>
                <br/>
                <img src={selectedFile} />
              </div>
              <br/>
              <br/>
              <button id="update_button" onClick = { controlUpload }>
                <b>Update</b>
              </button> 
              {Object.keys(summaries).length > 0 && (
                <div>
                  <h3>Summary:</h3>
                  {Object.keys(summaries).map(([section, summary]) => (
                    <div key={section}>
                      <h4>{section}</h4>
                      <p>{summary}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
        </div>
    </div>
  );
}

function EnterInfoPage() {
  return (
    <div className="App">
      <NavBar />
      <EnterInfo />
      <SidePencil />
      <BottomBanner />
    </div>
  );
}

export default EnterInfoPage;
