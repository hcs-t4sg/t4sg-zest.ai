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
import InputForm from './components/InputForm'
import MainNavBar from './components/MainNavBar'

function App() {
  const [placeholder, setPlaceholder] = useState("This is the default React message");

  useEffect(() => {
    fetch('http://localhost:5000/hello').then(res => res.json()).then(data => {
      setPlaceholder(data.result);
    });
  }, []);

  return (
    // In general, it's better to have a small return value with a lot of components that each live in their separate files
    // As a way of building out architecture, we've built out a bunch of empty components that you can fill out as you build out the front-end.
    // For any of these components, if you know of an existing library or component (ie: React bootstrap) that could work in place of one of the
    // components below, feel free to substitute it in!
    // This is just a skeleton. Feel free to get creative!

    // It may be helpful to look at Bootstrap and React-Bootstrap as you build out these components. 
    // Bootstrap: https://getbootstrap.com/ ; React-Bootstrap: https://react-bootstrap.github.io/
    <div className="App">
      <p>Is flask working: {placeholder}</p>
      <MainNavBar />

      <Description />

      <InputForm />

      <Display />

      <Footer />
    </div>
  );
}

export default App;