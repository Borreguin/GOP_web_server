
function create_legend(to_plot, legend_data, w_legend, h_legend, legend_colour) {

    let n_data = legend_data.length;

    // cleaning the space to work with
    d3.select(to_plot).select("svg").remove();
    d3.select(to_plot).select("img").remove();

    let legend = d3.select(to_plot)
        .append('div')
        .style("width", w_legend + "px")
        .style("height", h_legend + "px");

	// square size and text label size
	let icon_width = w_legend*0.08;
    let cell_height = h_legend/n_data;

    // let put the data inside the container
    // creating 'n_data' containers
    let container = legend.selectAll('.legend_panel')
        .data(legend_data, function(d) { return d.id; });

    // creating individual cells
    let cell = container.enter().append('div')
        .attr('class', 'container_legend')
        .style('height', (cell_height + 7) + "px")
        .style('width', w_legend + "px");


    // adding square icons for legends :
    let square = cell.append('div')
        .style('height', (cell_height) + "px")
        .style('width', icon_width + "px")
        .attr('class', 'square_legend')
        .style('background-color', function (d) {return legend_colour(d.id);});

    font_size_scale = scaleLinear({domain:[10, 24],range:[62.5, 170]});
    f_scale =  Math.max(70, font_size_scale(cell_height));
    // adding labels:
    let labels = cell.append('div')
        .attr("class", "text_legend")
        .style("color", "black")
        .style('height', cell_height + "px")
        .style("font-size", f_scale + "%")
        .style('width', (w_legend*0.97 - icon_width ) + "px" )
        .text(function (d) {
           return d.label;
        });

    // this avoids to overlapping
    let clear = cell.append('div')
        .attr("class", "clear");

}