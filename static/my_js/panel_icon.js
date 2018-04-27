let stripe_per_size = 0.5;
let stripe_class = "text_stripe";

function draw_panel(to_plot, data_panel) {

    let n_data = data_panel.length;

    // get width and height
    let borders = get_height_width(to_plot);
    let w_panel = borders.width; let h_panel = borders.height;

    // cleaning the space to work with
    d3.select(to_plot).select("svg").remove();
    d3.select(to_plot).select("img").remove();

	let gallery = d3.select(to_plot)
        .append('div')
        .style("width", (width + margin.left + margin.right) + "px")
        .style("height", (height + margin.top + margin.bottom) + "px");

	// icon size and cell size
	let icon_width = w_panel*0.30;
    let cell_height = h_panel/n_data;

    // let put the data inside the container
    // creating 'n_data' containers
    let container = gallery.selectAll('.container_panel')
        .data(data_panel, function(d) { return d.id; });

    // creating individual cells
    let cell = container.enter().append('div')
        .attr('class', 'container_panel')
        .style('height', cell_height + "px")
        .style('width', w_panel + "px")
        .style('border-color',function (d) {return d.color;} );

    // adding icons:
    let icons = cell.append('div')
        .attr("class", "rs_icon")
        .style('height', cell_height + "px");

    icons.append('img')
        .attr('class', 'img')
        .style("height", cell_height + "px")
        .attr('src', function(d) { return d.icon; });

    // adding stripes:
    let stripe_width = w_panel - icon_width - 3.5;
    let stripe_height = cell_height*stripe_per_size;
    let stripes = cell.append('div')
        .attr("class", "col-sm-8 btn btn-primary")
        .style('height', stripe_height + "px")
        .style('width', stripe_width + "px" )
        .style('background-color', function (d) {return d.color})
        .style('border-color', function (d) {return d.color})
        .append("xhtml:body")
        .style("background-color", "transparent")
        .html( function (d) {
            let font_size =  stripe_height*0.4;
            if(d.label.length > 18 && d.label.length < 24 ){
                font_size = stripe_height*0.35;
            }else if( d.label.length > 24){
                font_size = stripe_height*0.25;
            }
            return '<div' +
                ' style="width:'+ (stripe_width-10)  + 'px;' +
                ' font-size:'+ font_size +'px"' +
                ' class="' + stripe_class + '"' +
                '>'
                +  d.label
                + '</div>'});

    // adding value container:
    let value_cell = cell.append('div')
        .style('height', (cell_height - stripe_height) + "px")
        .style('width', stripe_width + "px")
        .attr("transform", "translate(" + icon_width + "," + stripe_per_size + ")");

    // adding stripes:

    /*let stripe = val_cell.append('rect')
        .attr('height', cell_height*stripe_per_size)
        .attr('width', stripe_width)
        .attr('fill', function (d) { return d.color; })
        .attr('fill-opacity', 0.9)
        .attr('stroke-width', 5)
        .attr('stroke', function (d) { return d.color; });*/

    /*let text = val_cell
        .append('foreignObject')
        .attr('x', w_panel*0.02)
        .attr('y', cell_height*0.02)
        .attr('width', stripe_width - 10)
        .attr('height', cell_height*0.7)
        .append("xhtml:body")
        .style("background-color", "transparent")
        .html( function (d) {
            return '<div' +
                ' style="width:'+ stripe_width  + 'px;"' +
                ' class="' + stripe_class + '"' +
                '><h4>'
                +  d.label
                + '</h4></div>'});



    /*
    //Add the SVG Text Element to the svgContainer
    let text = val_cell.append("text");

    //Add SVG Text Element Attributes
    let textLabels = text
        .attr("x", w_panel*0.05)
        .attr("y", cell_height*0.3)
        .text( function (d) { return d.label; })
        .attr("font-size", cell_height*0.2 + "px")
        .attr("class", "text_stripe")
        .attr("fill", "white");


    //container.exit().remove();

    /*
    indv_container.append('svg')
        .attr('class', 'value_panel')
        .attr("height", cell_height)
        .attr("transform", "translate(" + icon_width + "," + 0 + ")");*/

/*container.selectAll('.text')
    .data(function(d) { return [d]; })
    .enter().append('p')
    .attr('class', 'text')
    .text(function(d) { return d.id; });*/

    // Adding containers
    /*let svg_containers = container.enter()
        .append('svg')
        .attr('class', 'container')
        .attr("width",  width)
        .attr("height", cell_height)
        .attr("x",0)
        .attr("y", function (d) { return d.id*cell_height});*/



   /* container.selectAll('.picture')
    .data(function(d) { return [d]; })
    .enter().append('img')
    .attr('class', 'picture')
    .attr('src', function(d) { return d.icon; });*/

}

function plot_icons() {

    var data = [{id: 1, text: 'sample text 1', imgsrc: 'static/my_icons/electrical/foco.png'},
            {id: 2, text: 'sample text 2', imgsrc: 'static/my_icons/electrical/hidroelectrica.png'},
            {id: 3, text: 'sample text 3', imgsrc: 'static/my_icons/electrical/renovable.png'},
            {id: 4, text: 'sample text 4', imgsrc: 'static/my_icons/electrical/torre.png'}];

var gallery = d3.select(to_plot).append('div');

var container = gallery.selectAll('.container')
    .data(data, function(d) { return d.id; });

container.enter().append('div')
    .attr('class', 'container');

container.exit().remove();


container.selectAll('.text')
    .data(function(d) { return [d]; })
    .enter().append('p')
    .attr('class', 'text')
    .text(function(d) { return d.text; });

container.selectAll('.picture')
    .data(function(d) { return [d]; })
    .enter().append('img')
    .attr('class', 'picture')
    .attr('src', function(d) { return d.imgsrc; });
}