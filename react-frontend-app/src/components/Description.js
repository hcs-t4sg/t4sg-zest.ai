import React from 'react';
import '../style/Description.css';

// TO-DO: AUSTIN(?)

class Description extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className="description">
                <p> The <em>Zest Race Predictor (ZRP)</em> is an improved race prediction technology designed to <em>improve accountability</em> and <em>better facilitate fair lending</em>. This web application compares the ZRP with the current standard model used by the Consumer Financial Protection Bureau, BisG.

                    <br /><br /> By <em>Zest.Ai</em> and <em>Harvard Tech for Social Good</em></p>

            </div>
        )
    }
}


export default Description;