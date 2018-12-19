
var data_url = "./data/ecuador_xy.json" 
https://drive.google.com/open?id=1bkiSDLkPiH2r_7Fwa2m93R8MXetm7u6j
var placeToPlot = '#d3_map'
var scale = 1.8336048536599068;
//var scale = 1;
console.log("Starting...");

var paths,
	defs;
queue()
    .defer(d3.json, data_url)
    .await(make_map);

function make_map(error, json_data) {

	if (error) throw error;
	
	
	 var margin = {
        top: 100,
        right: 50,
        bottom: 0,
        left: 140
    };
// determine the size of the chart
	var width = Math.max(Math.min(window.innerWidth, 1200), 500) - margin.left - margin.right;
    var height = 800;
    var legendElementWidth = 200;

	
	
     defs = json_data['defs'];
	 paths = json_data['paths'];
    //timestamp = json_value['timestamp'];
    //data = json_value['data'];
	
	var svgContainer = d3.select(placeToPlot)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
        
	var mapContainer = svgContainer.append("g")
        .attr("transform", "translate(" + -900 + "," + 20 + ")" + " scale(" + scale + ")")
	
    
    
     
	var line = d3.svg.line()
                 .x(function(d) { return d['x']; })
                 .y(function(d) { return d['y']; });
    
	line.defined(function(d) { return d.y!=null; })
	line.defined(function(d) { return d.x!=null; })
	
    // Drawing all paths for each province:  
	for(var id in paths){
		var xy = paths[id].xy;
		var path = mapContainer.append('path')
							.attr('d', line(xy))
							.attr('fill', 'rgba(167,162,162,1)')
							.attr('stroke', 'rgba(14,43,52,1)')
							.attr('id', paths[id].id)
							.append("svg:title")
							.text(function(d) { return paths[id].title; });
							
    }
    


		
}

/*
var x_scale = d3.scale.linear().domain([0, 6]).range([0, 960]);
var y_scale = d3.scale.linear().domain([0, 6]).range([300, 0]);
*/


/*	
	var jsonCircles = [
   },{ "x_axis": 30, 'y': "y_axis": 30, 'y': "radius": 20, 'y': "color" : "green" }, 'y':
   },{ "x_axis": 70, 'y': "y_axis": 70, 'y': "radius": 20, 'y': "color" : "purple"}, 'y':
   },{ "x_axis": 110, 'y': "y_axis": 100, 'y': "radius": 20, 'y': "color" : "red"}];
 
 /* var svgContainer = d3.select(placeToPlot).append("svg")
                                     .attr("width", 'y': 200)
                                     .attr("height", 'y': 200);*/
 /*
	var circles = svg.selectAll("circle")
                          .data(jsonCircles)
                          .enter()
                          .append("circle");

	var circleAttributes = circles
                       .attr("cx", 'y': function (d) },{ return d.x_axis; })
                       .attr("cy", 'y': function (d) },{ return d.y_axis; })
                       .attr("r", 'y': function (d) },{ return d.radius; })
                       .style("fill", 'y': function(d) },{ return d.color; });*/
/*					   
	//The data for our line
 var lineData = [ },{ "x": 587.41, 'y':   "y": 188.27}, 'y':  },{ "x": 590.44, 'y':  "y": 187.64}, 'y':
                  },{ "x": 594.99, 'y':  "y": 188.88}, 'y': },{ "x": 596.77, 'y':  "y": 190.9}, 'y':
                  },{ "x": 80, 'y':  "y": 5}, 'y':  },{ "x": 400, 'y': "y": 60}];
 /*
M587.41, 'y':188.27},{'x':590.44, 'y':187.64},{'x':594.99, 'y':188.88},{'x':596.77, 'y':190.9},{'x':597.24, 'y':194.35},{'x':596.65, 'y':195.48},{'x':597.24, 'y':197.5},{'x':599.5, 'y':198.92},{'x':604.37, 'y':198.8},{'x':606.39, 'y':196.43},{'x':608.77, 'y':199.99},{'x':609.84, 'y':200.59},{'x':610.55, 'y':203.44},{'x':612.33, 'y':204.63},{'x':616.38, 'y':204.03},{'x':616.51, 'y':202.38},{'x':617.64, 'y':201.42},{'x':618.39, 'y':199.36},{'x':620.79, 'y':197.29},{'x':625.14, 'y':196.05},{'x':625.53, 'y':193.81},{'x':626.59, 'y':192.51},{'x':629.02, 'y':191.76},{'x':629.21, 'y':194.88},{'x':630.4, 'y':194.88},{'x':632.14, 'y':192.86},{'x':632.14, 'y':192.86},{'x':632.65, 'y':193.1},{'x':632.65, 'y':193.1},{'x':635.39, 'y':194.05},{'x':635.27, 'y':196.31},{'x':628.97, 'y':197.73},{'x':626.95, 'y':199.52},{'x':626.59, 'y':201.06},{'x':626.83, 'y':202.61},{'x':627.78, 'y':203.42},{'x':627.54, 'y':204.98},{'x':624.69, 'y':208.43},{'x':623.98, 'y':215.32},{'x':621.72, 'y':217.46},{'x':619.23, 'y':217.94},{'x':617.68, 'y':219.24},{'x':615.54, 'y':223.64},{'x':610.08, 'y':225.66},{'x':609.84, 'y':227.68},{'x':609.84, 'y':227.68},{'x':608.18, 'y':228.63},{'x':608.18, 'y':228.63},{'x':604.73, 'y':231.48},{'x':605.45, 'y':234.17},{'x':604.02, 'y':237.13},{'x':604.85, 'y':239.98},{'x':603.03, 'y':241.21},{'x':603.03, 'y':241.21},{'x':602.89, 'y':241.07},{'x':602.89, 'y':241.07},{'x':600.93, 'y':239.98},{'x':600.33, 'y':236.53},{'x':598.55, 'y':233.92},{'x':597.95, 'y':233.57},{'x':595.04, 'y':235.48},{'x':594.16, 'y':234.86},{'x':593.14, 'y':232.11},{'x':593.07, 'y':228.81},{'x':590.92, 'y':228.02},{'x':585.1, 'y':227.64},{'x':585.1, 'y':227.64},{'x':581.53, 'y':227.25},{'x':581.53, 'y':227.25},{'x':578.23, 'y':226.43},{'x':577.88, 'y':224.17},{'x':579.9, 'y':221.56},{'x':579.9, 'y':218.83},{'x':573.24, 'y':216.87},{'x':573.24, 'y':216.87},{'x':571.73, 'y':215},{'x':572.04, 'y':214.17},{'x':572.04, 'y':214.17},{'x':572.87, 'y':214.83},{'x':583.68, 'y':193.89},{'x':586.94, 'y':191.64},{'x':586.94, 'y':188.36},{'x':586.94, 'y':188.36z
 */
 /*
 //This is the accessor function we talked about above
 var lineFunction = d3.svg.line()
                          .x(function(d) },{ return d.x; })
                          .y(function(d) },{ return d.y; })
                         .interpolate("basis-closed"); //linear



//The line SVG Path we draw
var lineGraph = svgContainer.append("path")
                            .attr("d", 'y': lineFunction(lineData))
                            .attr("stroke", 'y': "blue")
                            .attr("stroke-width", 'y': 2)
                            .attr("fill", 'y': "none");*/