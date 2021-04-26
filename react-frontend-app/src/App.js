// Import pre-existing react libraries
import React, { useState } from 'react';
import axios from 'axios';

// Import stylesheet
import 'bootstrap/dist/css/bootstrap.css';
import './style/App.css';

// Import different components
import Description from './components/Description'
import Footer from './components/Footer'
import MainNavBar from './components/MainNavBar'
import BarGraph from './components/BarGraph'
import Button from 'react-bootstrap/Button';
// import Container from 'react-bootstrap/Container';
// import Form from 'react-bootstrap/Form';
// import { Col } from 'react-bootstrap';

function App() {

  const [loading, setLoading] = useState(true);

  // bisgData stores probabilities from bisg
  var [bisgData, setbisgData] = useState('default bisg');
  console.log("bisgData: ", bisgData);
  // zrpData stores probs from zrp model
  var [zrpData, setzrpData] = useState('default zrp');
  console.log("zrpData: ", zrpData);

  const [allValues, setAllValues] = useState({
    first_name: '',
    middle_name: '',
    last_name: '',
    gender: '',
    age: '',
    street_address: '',
    city: '',
    state: '',
    zipcode: ''
  });

  // Functions that are called whenever the text input is changed
  function changeHandler(e) {
    setAllValues({ ...allValues, [e.target.name]: e.target.value })
  }

  // Function that called when the submit button is pressed
  async function handleSubmit(event) {
    event.preventDefault();
    axios.get(`http://localhost:5000/surgeo?surname=${allValues.last_name}&zipcode=${allValues.zipcode}`)
      .then(res => {
        setbisgData(res.data);
        console.log("bisgData has been updated: ", res.data);
      });
    axios.get(`http://localhost:5000/zrp?first_name=${allValues.first_name}&middle_name=${allValues.middle_name}&last_name=${allValues.last_name}&gender=${allValues.gender}&age=${allValues.age}&street_address=${allValues.street_address}&city=${allValues.city}&state=${allValues.state}&zipcode=${allValues.zipcode}`)
      .then(res => {
        setzrpData(res.data);
        console.log("zrpData has been updated: ", res.data);
      });
    axios.get(`https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML=<AddressValidateRequest USERID="658HARVA0117"><Address ID="0"><Address1>5330 N Luna St</Address1><Address2/><City>Chicago</City><State>IL</State><Zip5>60630</Zip5><Zip4/></Address></AddressValidateRequest>`)
      .then(res => {
        console.log("address validation chicago example: ", res.data);
    });
    setLoading(false);
  }

  return (
    <div className="App">
      <MainNavBar />

      <h1>Zest Race Predictor</h1>
      <br />
      <Description />
      <hr style={{
        width: "50%"
      }}></hr>
      < form onSubmit={handleSubmit} >
      <label> Please enter your information: </label>
      <br /> <br />
      First name: <input type="text" name="first_name" onChange={changeHandler} /> <br /> <br />
      Middle name: <input type="text" name="middle_name" onChange={changeHandler} /> <br /> <br />
      Last name: <input type="text" name="last_name" onChange={changeHandler} /> <br /> <br />
      Gender: <input type="text" name="gender" onChange={changeHandler} /> <br /> <br />
      Age: <input type="text" name="age" onChange={changeHandler} /> <br /> <br />
      Street address: <input type="text" name="street_address" onChange={changeHandler} /> <br /> <br />
      City: <input type="text" name="city" onChange={changeHandler} /> <br /> <br />
      State: <input type="text" name="state" onChange={changeHandler} /> <br /> <br />
      Zip code: <input type="text" name="zipcode" onChange={changeHandler} /> <br /> <br />
      <Button type="submit" value="Submit">Submit</Button>
      </form>
      <br/>
      { (bisgData == 'default bisg' || loading) 
        ? <div> <h3>Nothing here, submit your data!</h3> </div>
        : <div className="svg-class"><h3>Breakdown</h3> <BarGraph white={bisgData.white[0]} 
        black={bisgData.black[0]} api={bisgData.api[0]} hispanic={bisgData.hispanic[0]} 
        multiple={bisgData.multiple[0]} native={bisgData.native[0]} zrpWhite={zrpData["White"]}
        zrpBlack={zrpData["Black"]} zrpApi={zrpData["Asian Pacific Islander"]} zrpHispanic={zrpData["Hispanic"]}
        zrpMulti={zrpData["Multi"]} zrpNative={zrpData["American Indian"]} /> </div> 
      }
      <Footer />
    </div>
  );
}

export default App;