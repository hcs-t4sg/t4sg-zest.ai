import React from 'react';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

export class Form extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            race : 'default race'
        };

        this.componentDidMount = this.componentDidMount.bind(this);
    }

  componentDidMount() {

    axios.get(`http://127.0.0.1:5000/bisg`
    )
      .then(res => {
        console.log("this is form res");
        console.log(res);
        // const race = res.[0]].text;
        // console.log(race);
        // this.setState({ race });
      })
  }

  render() {
    return (
        <div>
            <form method='get'>
                <h3>Surname:</h3>
                <input type="text"/>
                <h3>Zipcode:</h3>
                <input type="text"/>
                <br/>
                <br/>
                <Button onClick={this.componentDidMount}>Run Model</Button>
            </form>
            
            <br/>
            <br/>
        </div>
    )
  }
}