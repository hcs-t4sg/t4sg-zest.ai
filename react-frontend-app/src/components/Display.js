import React from 'react';
import '../style/Display.css';

// TO-DO: KAYLA(?)
// Build out a display object that takes in the probabilities of each race prediction as a key-value pair object (json-like)
// and displays them in the style of the WSJ

class Display extends React.Component {
    constructor(props) {
        super(props)
        // You should store stateful data (ie: the probabilities of each race)
        this.state = {}
    }

    render () {
        return (
            <div>
                <p>I am the display component that will display the probabilities of each race. I'm very sad b/c I have no code here yet</p>
            </div>
        )
    }
}


export default Display;