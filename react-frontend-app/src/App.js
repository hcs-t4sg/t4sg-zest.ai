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
import Footer from './components/Footer'
import MainNavBar from './components/MainNavBar'
import BarGraph from './components/BarGraph'

function App() {
  const [surname, setSurname] = useState('');
  const [zipcode, setZip] = useState('');
  const [loading, setLoading] = useState(true);

  // bisgData stores probabilities from bisg
  var [bisgData, setbisgData] = useState('default bisg');

  // Functions that are called whenever the text input is changed
  function handleSurname(event) {
    setSurname(event.target.value);
  }

  function handleZip(event) {
    setZip(event.target.value);
  }

  // Function that called when the submit button is pressed
  async function handleSubmit(event) {
    event.preventDefault();

    await axios.get(`http://localhost:5000/surgeo?surname=${surname}&zipcode=${zipcode}`)
      .then(res => {
        setbisgData(res.data);
        console.log("axios retrieved: ");
        console.log(res.data);
        console.log(bisgData);
      });
    setLoading(false);
  }

  return (
    <div className="App">
      <MainNavBar />
      <br /><br /><br /><br /><br />
      <h1>Zest AI Race Predictor Prototype</h1>
      <br />
      <Description />
      <form onSubmit={handleSubmit}>
        <label>Please enter your information:</label>
        <br /><br />
        Surname: <input type="text" onChange={handleSurname} />
        <br /><br />
        Zip code: <input type="text" onChange={handleZip} />
        <br /><br />
        <Button type="submit" value="Submit">submit</Button>
      </form>
      <br />
      { (bisgData == "default bisg" || loading) 
        ? <div> <h3>Nothing here, submit your data!</h3> </div>
        : <div><h3>Breakdown</h3> <BarGraph white={bisgData.white[0]} black={bisgData.black[0]} api={bisgData.api[0]} hispanic={bisgData.hispanic[0]} multiple={bisgData.multiple[0]} native={bisgData.native[0]} /> </div> 
      }
      <Footer />
    </div>
  );
}

export default App;