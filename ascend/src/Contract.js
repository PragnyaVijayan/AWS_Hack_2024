import './Contract.css';
import upload from './imgs/upload.png';
import React, { useState} from 'react';
import axios from 'axios';

function App() {
  
  // State to store uploaded file
  const [selectedFile, setSelectedFile] = useState(null);

  function controlChange(e) {
    setSelectedFile(URL.createObjectURL(e.target.files[0]));
  }

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
                <input type="file" id = "file_input" onChange={ controlChange } style={{ display: 'none' }}/>
                <br/>
                <br/>
                <img src={selectedFile} />
                
              </div>
              <br/>
              <br/>
              {/* <button id="update_button" onClick = { controlUpload }>
                <b>Update</b>
              </button> */}
            </div>
        </div>
    </div>
  );
}

export default App;