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
  const [allValues, setAllValues] = useState({
    zipcode: '',
    last_name: '',
    first_name: '',
    middle_name: '',
    precinct_split: '',
    gender: '',
    county_code: '',
    congressional_district: '',
    senate_district: '',
    house_district: '',
    birth_date: ''
  });

  // Functions that are called whenever the text input is changed
  function changeHandler(e) {
    setAllValues({...allValues, [e.target.name]: e.target.value})
  }

  // Function that called when the submit button is pressed
  function handleSubmit(event) {
    event.preventDefault();
    axios.get(`http://localhost:5000/surgeo?surname=${allValues.last_name}&zipcode=${allValues.zipcode}`)
      .then(res => console.log(res.data));
    axios.get(`http://localhost:5000/zrp?zipcode=${allValues.zipcode}&first_name=${allValues.first_name}&last_name=${allValues.last_name}&middle_name=${allValues.middle_name}&precinct_split=${allValues.precinct_split}&gender=${allValues.gender}&county_code=${allValues.county_code}&congressional_district=${allValues.congressional_district}&house_district=${allValues.house_district}&birth_date=${allValues.birth_date}&senate_district=${allValues.senate_district}`)
      .then(res => console.log(res.data));
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
        First Name: <input type="text" name="first_name" onChange={changeHandler}/><br/><br/>
        Middle Name: <input type="text" name="middle_name" onChange={changeHandler}/><br/><br/>
        Surname: <input type="text" name="last_name" onChange={changeHandler}/><br/><br/>
        Gender: <input type="text" name="gender" onChange={changeHandler}/><br/><br/>
        Birthday: <input type="text" name="birth_date" onChange={changeHandler}/><br/><br/>
        Zip code: <input type="text" name="zipcode" onChange={changeHandler}/><br/><br/>
        Precinct split: <input type="text" name="precinct_split" onChange={changeHandler}/><br/><br/>
        County code: <input type="text" name="county_code" onChange={changeHandler}/><br/><br/>
        Congressional district: <input type="text" name="congressional_district" onChange={changeHandler}/><br/><br/>
        Senate district: <input type="text" name="senate_district" onChange={changeHandler}/><br/><br/>
        House district: <input type="text" name="house_district" onChange={changeHandler}/><br/><br/>
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