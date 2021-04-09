// Import pre-existing react libraries
import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';

// Import image files
import logo from './logo.svg';

// Import stylesheet
import './style/App.css';

// Import different components
import Description from './components/Description'
import Display from './components/Display'
import Footer from './components/Footer'
import MainNavBar from './components/MainNavBar'
import BarGraph from './components/BarGraph'

function App() {
  const [surname, setSurname] = useState('');
  const [zipcode, setZip] = useState('');

  // ZRP inputs
  const [firstName, setFirst] = useState('');
  const [midName, setMid] = useState('');
  const [precinct, setPrecinct] = useState('');
  const [gender, setGender] = useState('');
  const [county, setCounty] = useState('');
  const [cong, setCong] = useState('');
  const [senate, setSenate] = useState('');
  const [house, setHouse] = useState('');
  const [birth, setBirth] = useState('');

  // Functions that are called whenever the text input is changed
  function handleSurname(event) {
    setSurname(event.target.value);
  }
  function handleZip(event) {
    setZip(event.target.value);
  }
  function handlefirstName(event) {
    setFirst(event.target.value);
  }
  function handlemidName(event) {
    setMid(event.target.value);
  }
  function handlePrecinct(event) {
    setPrecinct(event.target.value);
  }
  function handleGender(event) {
    setGender(event.target.value);
  }
  function handleCounty(event) {
    setCounty(event.target.value);
  }
  function handleCong(event) {
    setCong(event.target.value);
  }
  function handleSenate(event) {
    setSenate(event.target.value);
  }
  function handleHouse(event) {
    setHouse(event.target.value);
  }
  function handleBirth(event) {
    setBirth(event.target.value);
  }

  // Function that called when the submit button is pressed
  function handleSubmit(event) {
    event.preventDefault();
    console.log('Submit was pressed');
    var promise = new Promise((resolve) => {
        axios.get(`http://localhost:5000/surgeo?surname=${surname}&zipcode=${zipcode}`)
        .then(res => console.log(res.data))
        .then(axios.get(`http://localhost:5000/zrp?zipcode=${zipcode}&first_name=${firstName}&last_name=${surname}&middle_name=${midName}&precinct_split=${precinct}&gender=${gender}&county_code=${county}&congressional_district=${cong}&house_district=${house}&birth_date=${birth}&senate_district=${senate}`))
        .then(res => console.log(res))
      resolve(true)
    }
    );
    // promise.then(
    //   axios.get(`http://localhost:5000/zrp?zipcode=${zipcode}&first_name=${firstName}&last_name=${surname}&middle_name=${midName}&precinct_split=${precinct}&gender=${gender}&county_code=${county}}&congressional_district=${cong}&house_district=${house}&birth_date=${birth}&senate_district=${senate}`)
    //   .then(res => console.log(res))
    // );
  }

  return (
    <div className="App">
      <MainNavBar />
      <br/><br/><br/><br/><br/>
      <h1>Zest AI Race Predictor Prototype</h1>
      <br/>
      <Description />
      <form onSubmit={handleSubmit}>
        <label>Please enter your information:</label>
        <br/><br/>
        First Name: <input type="text" onChange={handlefirstName}/><br/><br/>
        Middle Name: <input type="text" onChange={handlemidName}/><br/><br/>
        Surname: <input type="text" onChange={handleSurname}/><br/><br/>
        Gender: <input type="text" onChange={handleGender}/><br/><br/>
        Birthday: <input type="text" onChange={handleBirth}/><br/><br/>
        Zip code: <input type="text" onChange={handleZip}/><br/><br/>
        Precinct split: <input type="text" onChange={handlePrecinct}/><br/><br/>
        County code: <input type="text" onChange={handleCounty}/><br/><br/>
        Congressional district: <input type="text" onChange={handleCong}/><br/><br/>
        Senate district: <input type="text" onChange={handleSenate}/><br/><br/>
        House district: <input type="text" onChange={handleHouse}/><br/><br/>
        <Button type="submit" value="Submit">submit</Button>
      </form>
      <br/>
      <div>
        <h4>Breakdown</h4>
        <BarGraph />
      </div>

      {/* Also in progress */}
      {/* <Display /> */}
      <Footer />
    </div>
  );
}

export default App;