// importing packages + functions we need
import reportWebVitals from "./../reportWebVitals.js";

import React, { Component } from "react";
import * as d3 from "d3";
import { select, selectAll, mouse } from "d3-selection";

// import some data at some point
// var data = {"zcta5":{"0":"02138"},"name":{"0":"HUANG"},"white":{"0":0.0032185893},"black":{"0":0.0001859026},"api":{"0":0.9874016372},"native":{"0":0.0000140781},"multiple":{"0":0.0087119711},"hispanic":{"0":0.0004678217}};

// constants go here

class BarGraph extends Component {

    constructor(props) {
        super(props);
        // this.state = {
        //     school: "Harvard",
        //     year: "2020",
        // };
        this.createBar = this.createBar.bind(this);
    }

    componentDidMount() {
        const res = await fetch('http://0.0.0.0:5000/surgeo');
        const data = await res.json();

        this.createBar(data);
    }

    // componentDidUpdate() {
    //     var schools;
    //     var data;
    //     // if (this.state.year === "2020") {
    //     //     data = data2020;
    //     //     schools = schools2020;
    //     // } else {
    //     //     data = data2019;
    //     //     schools = schools2019;
    //     // }

    //     if (!schools.includes(this.state.school)) {
    //         if (this.state.year === "2020") {
    //             this.setState({ school: "Harvard" });
    //             this.createBar(data["Harvard"]);
    //         } else {
    //             this.setState({ school: "Harvard University" });
    //             this.createBar(data["Harvard University"]);
    //         }
    //     } else {
    //         this.createBar(data[this.state.school]);
    //     }
    // }

    // handleInputChange = (event) => {
    //     const { name, value } = event.target;
    //     this.setState({ [name]: value });
    // };

    createBar(data) {
        var margin = { top: 30, right: 30, bottom: 50, left: 30 };
        var width = 700 - margin.left - margin.right;
        var height = width;
        console.log("inside the GraphBar.js file: ");
        console.log(data);

        var svg = d3
            .select("body")
            .append("svg")
            .attr("id", "chart-area")
            .style("width", width + 'px')
            .style("height", height + 'px')
            // .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .append("g");
        
    }
}

export default BarGraph;