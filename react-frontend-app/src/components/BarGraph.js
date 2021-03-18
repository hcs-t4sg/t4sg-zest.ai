// import all packages
import reportWebVitals from "./../reportWebVitals.js";
import React, { Component } from "react";
import { max, descending, schemeCategory10, version, schemePastel1 } from "d3";
import { scaleOrdinal, scaleLinear } from "d3-scale";
import { axisLeft } from "d3-axis";
import { select, selectAll } from "d3-selection";
import { format } from "d3-format";
import '../style/App.css';

// import axios from "axios";
// goal is to pass in data from the api call (currently, this is dummy data)
var data = {
    "white": {
        "bisg": "0.6700283648",
        "zest": "0.6180442684"
    },
    "black": {
        "bisg": "0.0033692506",
        "zest": "0.0153741615"
    },
    "api": {
        "bisg": "0.309192341",
        "zest": "0.3543504815"
    },
    "native": {
        "bisg": "0.0019506335",
        "zest": "0.0010750276"
    },
    "multiple": {
        "bisg": "0.0064047544",
        "zest": "0.0093698772"
    },
    "hispanic": {
        "bisg": "0.0090546558",
        "zest": "0.0017861839"
    }
};

const d3 = {
    select,
    selectAll,
    descending,
    schemeCategory10,
    version,
    scaleOrdinal,
    scaleLinear,
    max,
    axisLeft,
    format,
    schemePastel1
};

class BarGraph extends React.Component {

    constructor(props) {
        super(props);
        this.createBar = this.createBar.bind(this);
    }

    async componentDidMount() {
        // const res = await axios.get('http://0.0.0.0:5000/surgeo');
        // const data = await res.json();
        
        this.createBar(data);
    }

    componentDidMount() {
        this.createBar(data);
    }
    componentDidUpdate() {
        this.createBar(data);
    }

    createBar(data) {

        var chartWidth       = 300,
            barHeight        = 20,
            groupHeight      = barHeight * 2,
            gapBetweenGroups = 10,
            spaceForLabels   = 150,
            spaceForLegend   = 150;
        
        var zippedData = [];
        var races = ["white", "black", "api", "native", "multiple", "hispanic"];
        var racesCaps = ["White", "Black", "Asian/PI", "Native", "Multiple", "Hispanic"];
        for (var i=0; i<6; i++) {
            zippedData.push(parseFloat(data[races[i]].bisg));
            zippedData.push(parseFloat(data[races[i]].zest));
        }

        var margin = { top: 30, right: 30, bottom: 50, left: 30 };
        var width = 700 - margin.left - margin.right;
        var height = width;

        var svg = d3
            .select("body")
            .append("svg")
            .attr("id", "chart-area")
            .style("width", width + 'px')
            .style("height", height + 'px')
            .attr("transform", "translate(" + (width / 2 - 10) + "," + 10 + ")")
            .attr("viewBox", [-50, -50, width + 50, height + 50])
            .append("g");


        var color = d3.scaleOrdinal(d3.schemePastel1);
        var chartHeight = barHeight * 12 + gapBetweenGroups * 6;

        var x = d3.scaleLinear()
            .domain([0, d3.max(zippedData)])
            .range([0, chartWidth]);

        var y = d3.scaleLinear()
            .range([chartHeight + gapBetweenGroups, 0]);

        var yAxis = d3.axisLeft(y)
            .tickFormat('')
            .tickSize(0);

        // Specify the chart area and dimensions
        var chart = svg.selectAll("g") //d3.select(".chart-area") // ".chart"
            .attr("width", spaceForLabels + chartWidth + spaceForLegend)
            .attr("height", chartHeight);

        // Chart title
        svg.append("text")
            .attr("x", (width / 2))             
            .attr("y", -30)
            .attr("text-anchor", "middle")  
            .style("font-size", "16px") 
            .style("font-weight", "bold")
            .text("Full Race Prediction Model Results");

        // Create bars
        var bar = svg.selectAll("g")
            .data(zippedData)
            .enter()
            .append("g")
            .attr("transform", function(d, i) { 
                return "translate(" + spaceForLabels + "," + (i * barHeight + gapBetweenGroups * (0.5 + Math.floor(i/2))) + ")";
            });
        
        // Create rectangles of the correct width
        bar.append("rect")
            .attr("fill", function(d,i) { return color(i % 2); })
            .attr("class", "bar")
            .attr("width", x)
            .attr("height", barHeight - 1);

        // Add text label in bar
        bar.append("text")
            .attr("x", function(d) { return x(d) + 5; })
            .attr("y", barHeight / 2)
            .attr("font-size", "10px")
            .attr("fill", "black")
            .attr("dy", ".35em")
            .text(function(d) { return d3.format(".2%")(d); });

        // Draw labels
        bar.append("text")
            .attr("class", "label")
            .attr("x", function(d) { return - 20; })
            .attr("text-anchor", "end")  
            .attr("y", groupHeight / 2)
            .attr("dy", ".35em")
            .text(function(d,i) {
                if (i % 2 === 0)
                    return racesCaps[Math.floor(i/2)];
                else
                    return "";
            });

        // Display y-axis
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + spaceForLabels + ", " + -gapBetweenGroups/2 + ")")
            .call(yAxis);
        
        // Draw legend/key
        var legendRectSize = 18,
            legendSpacing  = 4;

        var legend = svg.selectAll('.legend')
            .data(["BISG Model", "Zest Model"])
            .enter()
            .append('g')
            .attr('transform', function (d, i) {
                var height = legendRectSize + legendSpacing;
                var offset = -gapBetweenGroups/2;
                var horz = spaceForLabels + chartWidth + 100 - legendRectSize;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });

        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', function (d, i) { return color(i); })
            .style('stroke', function (d, i) { return color(i); });

        legend.append('text')
            .attr('class', 'legend')
            .attr('x', legendRectSize + legendSpacing + 3)
            .attr('y', legendRectSize - legendSpacing)
            .attr("font-size", "12px")
            .attr("fill", "black")
            .text(function (d) { return d; });

    }
    render() {
        return "";
    }
}

export default BarGraph;
reportWebVitals();
