import React from 'react';
import '../style/MainNavBar.css';
import logo from '../zest_logo.png';
import { color } from 'd3';

function MainNavBar() {
    return (
        <div className="container" style={{ backgroundColor: "#01222D", width: "100%" }}>
            <div className="logo">
                <a href="#"><img src={logo} /></a>
            </div>
        </div >
    )
}

export default MainNavBar;