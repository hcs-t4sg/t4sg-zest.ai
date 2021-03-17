// Import pre-existing react libraries
import React, { useState, useEffect } from 'react';

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

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {placeholder: "This is the default React message", input_val: ""}
  }

  // Function that is called when the app first starts
  componentDidMount() {
    fetch('http://localhost:5000/hello').then(res => res.json()).then(data => {
      this.setState({placeholder: data.result});
    });
  }

  // Function that is called whenever the text input is changed
  handleChange(event) {
    this.setState({input_val: event.target.value});
  }

  // Function that called when the submit button is pressed
  handleSubmit(event) {
    event.preventDefault();
    console.log('Submit was pressed')
  }

  render() {
    // In general, it's better to have a small return value with a lot of components that each live in their separate files
    // As a way of building out architecture, we've built out a bunch of empty components that you can fill out as you build out the front-end.
    // For any of these components, if you know of an existing library or component (ie: React bootstrap) that could work in place of one of the
    // components below, feel free to substitute it in!
    // This is just a skeleton. Feel free to get creative!

    // It may be helpful to look at Bootstrap and React-Bootstrap as you build out these components. 
    // Bootstrap: https://getbootstrap.com/ ; React-Bootstrap: https://react-bootstrap.github.io/
    return (
      <div className="App">
        <p>Is flask working: {this.state.placeholder}</p>

        <MainNavBar />

        <Description />

        <form onSubmit={this.handleSubmit}>
            <label>
              Insert Form Information:
            <input type="text" value={this.state.input_val} onChange={this.handleChange}/>
            </label>
            <input type="submit" value="Submit" />
        </form>

        <BarGraph />

        <Display />

        <Footer />
      </div>
    );
  }
}

export default App;