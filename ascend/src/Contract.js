import './Contract.css';
import upload from './imgs/upload.png';
import React, { useState} from 'react';
import axios from 'axios';

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


export default Contract;