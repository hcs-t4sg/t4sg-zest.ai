import React from 'react';
import '../style/MainNavBar.css';
import logo from '../zest_logo.png';

function MainNavBar() {
    return (
        <div className="container">
            <nav>
                <input type="checkbox" id="nav" className="hidden"/>
                <label htmlFor="nav" className="nav-btn">
                    <i></i>
                    <i></i>
                    <i></i>
                </label>
                <div className="logo">
                    <a href="#"><img src={logo}/></a>
                </div>
                <div className="nav-wrapper">
                    <ul>
                        <li><a href="#">About</a></li>
                    </ul>
                </div>
            </nav>
        </div>
    )
}

export default MainNavBar;