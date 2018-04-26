/* ########################################################################### */
// The following are parameter by default:

let placeToPlot = '#d3_map';
const defs = map_data['defs'],
    paths = map_data['paths'],
    colors = map_config;

let scale = 1,
    map_center_x = 20,
    map_center_y = 10;

let margin = {
        top: 5,
        right: 10,
        bottom: 5,
        left: 10
};

let bar_size = 160;
let w = $(document).width();
let h = $(document).height();
let height =  Math.max(Math.min(h, 800), 300) - margin.top - margin.bottom - bar_size;
let width = Math.max(Math.min(w, 1200), 500) - margin.left - margin.right;


/* ########################################################################### */


// It allows to re-define parameters for this chart:
function define_map(new_margin, new_width, new_height) {
    margin = new_margin;
    width = new_width;
    height = new_height;
}


function make_map(to_plot, to_select) {

    placeToPlot = to_plot;

    // get width and height
    let borders = get_height_width(to_plot);
    width = borders.width; height = borders.height;

    // cleaning the space to work with
    d3.select(to_plot).select("svg").remove();
    d3.select(to_plot).select("img").remove();

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

                x_scale = d3.scale.linear()
                    .domain([paths[to_select].minX, paths[to_select].maxX])
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
    d3.selectAll(".province").on("dblclick",function(){
        let color = this.attributes.fill.value;
        make_map(placeToPlot, this.id);
        d3.select("#"  + this.id).attr('fill', color);
    });
}
/*
function create_home_button() {

}*/