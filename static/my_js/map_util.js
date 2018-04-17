/* ########################################################################### */
// The following are parameter by default:

const placeToPlot = '#d3_map',
    defs = map_data['defs'],
    paths = map_data['paths'],
    colors = map_config;

let scale = 1,
    map_center_x = 25,
    map_center_y = 20;

let margin = {
        top: 10,
        right: 10,
        bottom: 10,
        left: 10
};

// determine the size of the chart
let width = Math.max(Math.min(window.innerWidth, 1200), 500) - margin.left - margin.right;
let height =  Math.max(Math.min(window.innerHeight, 1000), 500) - margin.top - margin.bottom;

/* ########################################################################### */


// It allows to re-define parameters for this chart:
function define_map(new_margin, new_width, new_height) {
    margin = new_margin;
    width = new_width;
    height = new_height;
}


console.log("Starting Ecuador map...");
make_map(placeToPlot, map_selection);
assign_color(colors);
assign_function();

function make_map(to_plot, to_select) {

    d3.select(to_plot).select("svg").remove();

	let svgContainer = d3.select(placeToPlot)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
        
	let mapContainer = svgContainer.append("g")
        .attr("transform", "translate(" + map_center_x + "," + map_center_y + ")" + " scale(" + scale + ")");


	let x_scale = d3.scale.linear()
        .domain([defs["left"], defs["right"]])
        .range([margin.left, width - margin.right]);

	let y_scale = d3.scale.linear()
        .domain([defs["top"] , defs["bottom"]])
        .range([margin.top, height-margin.bottom]);

	let line = d3.svg.line()
                 .x(function(d) { return x_scale(d['x']); })
                 .y(function(d) { return y_scale(d['y']); });
    
	line.defined(function(d) { return d.y!=null; });
	line.defined(function(d) { return d.x!=null; });


    // Drawing all paths for each province:
    for(let id in paths){
        let xy;
        if (to_select === "all") {
            xy = paths[id].xy;
        }
        else {
            if(id !== to_select){ continue; }
            try {
                xy = paths[to_select].xy;
                let minx = paths[to_select].minX;
                let miny = paths[to_select].minY;
                let maxy = paths[to_select].maxY;
                let maxx = paths[to_select].maxX;

                x_scale = d3.scale.linear()
                    .domain([paths[to_select].minX , paths[to_select].maxX])
                    .range([margin.left, width - margin.right]);

                y_scale = d3.scale.linear()
                    .domain([paths[to_select].minY , paths[to_select].maxY])
                    .range([margin.top, height-margin.bottom]);

            } catch (err) {
                console.log(err);
                return -1;
            }
        }
        mapContainer.append('path')
            .attr('d', line(xy))
            .attr('fill', 'rgba(167,162,162,1)')
            .attr('stroke', 'rgba(14,43,52,1)')
            .attr('id', paths[id].id)
            .attr('class', "province")
            .append("svg:title")
            .text(function() { return paths[id].title; });
    }
}

function assign_color(map_information) {
    for(let id in map_information){
        d3.select("#"  + id).attr('fill', map_information[id].color);
    }
}

function assign_function() {
    d3.selectAll(".province").on("dblclick",function(d){
        make_map(placeToPlot, this.id);
    });
}