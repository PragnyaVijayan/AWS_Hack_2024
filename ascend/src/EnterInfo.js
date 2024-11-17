import './App.css';
import NavBar from './Components/Navbar';
import BottomBanner from './Components/BottomBanner';
import sidePencilImg from './Assets/Home/logo stretch.png'
import React, { useState } from "react";

function SidePencil() {
  return (
    <img className="SidePencil2" src={sidePencilImg} alt=""/>
  );
}

function EnterInfo() {
  const [jobInputVal, setJobInputVal] = useState("");
  const [yearsInputVal, setYearsInputVal] = useState("");
  const [skillInputVal, setSkillInputVal] = useState("");
  const [salaryInputVal, setSalaryInputVal] = useState("");
  const [stateInputVal, setStateInputVal] = useState("");
  const [pastSalaryInputVal, setPastSalaryInputVal] = useState("");

  const handleSubmit = () => {
    // TODO: put into S3
    alert(`Input Value: ${jobInputVal + yearsInputVal + skillInputVal + salaryInputVal + stateInputVal + pastSalaryInputVal}`); 
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
    <h2>I currently work with </h2>
    <input type="text" value={skillInputVal} onChange={(event) => setSkillInputVal(event.target.value)} name="myInput" className="userInput skillInput" />
    <h2>.</h2>

    <br></br>
    <h2>My desired salary is </h2>
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

    <button onClick={handleSubmit} className="ContinueBtn">Continue</button>
  </div>;
}

function EnterInfoPage() {
  return (
    <div className="App">
      <NavBar />
      <EnterInfo />
      {/* TODO: add back in <SidePencil /> */}
      <BottomBanner />
    </div>
  );
}

export default EnterInfoPage;
