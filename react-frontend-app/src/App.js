import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import { Form } from './components/form';

function App() {
  const [placeholder, setPlaceholder] = useState("This is the default React message");

  useEffect(() => {
    fetch('/hello').then(res => res.json()).then(data => {
      setPlaceholder(data.result);
    });
  }, []);

  const [value, setValue] = useState('');
  const [zip, setZip] = useState('zip default');

  function handleSubmit(e) {
    e.preventDefault();
    const data = { name: value, zipcode: zip };
    console.log('submitted value:');
    console.log(value);
    fetch('http://127.0.0.1:5000/test/', {
      method: 'POST',
      // mode: 'no-cors',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(res => res.json())
      .then(res => {
        console.log("this is test res: ");
        console.log(res);
        setValue(res.name.name);
        setZip(res.name.name);
      });
  }

  function handleValue(e) {
    setValue(e.target.value);
  }

  function handleValue2(e) {
    setZip(e.target.zip);
  }

  return (
    <div className="App">
      <br/><br/><br/><br/><br/>
      <h1>t4sg zest.ai BISG model</h1>
      <p>testing flask connection: {placeholder}.</p>
      <br/>
      <br/>
      <h2>the SURGEO api:</h2>
      
      {/* <Form/>
      <br />
      <br /> */}

      <br/>
      <br/>
      <h2>communication w backend from starter project:</h2>
      <br/>
      <form action="" onSubmit={handleSubmit}>
          <h3>Surname:</h3>
          <input type="text" onChange={handleValue}/>
          <h3>Zipcode:</h3>
          <input type="text" onChange={handleValue2}/>
          <br/>
          <br/>
        {/* <input type="text" onChange={handleValue} /> */}
        <button> submit </button>
      </form>
      <p>the word is: {value}</p>

    </div>
  );
}

export default App;