/**
 * Created by Roberto on 5/1/2018.
 * Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
 * Mateo 6:33
 */

let stripe_per_size = 0.5;
let stripe_class = "text_stripe";
let value_class = "value_stripe";

function draw_panel(to_plot, data_panel, callback) {

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
    let cell_height = Math.min(h_panel/n_data, 100);

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
        .style('height', (cell_height + 2) + "px");

    icons.append('img')
        .attr('class', 'img')
        .style("height", (cell_height + 10) + "px")
        .attr('src', function(d) { return d.icon; });

    // adding stripes:
    let stripe_width = w_panel - icon_width - 2.9;
    let stripe_height = cell_height*stripe_per_size;
    let stripes = cell.append('div')
        .attr("class", "col-sm-8 btn btn-primary")
        .style('height', stripe_height + "px")
        .style('width', stripe_width + "px" )
        .style('padding', 2 + "px" )
        .style('background-color', function (d) {return d.color})
        .style('border-color', function (d) {return d.color})
        .append("xhtml:body")
        .style("background-color", "transparent")
        .html( function (d) {
            let y_scale = scaleLinear({domain:[200 , 1000], range: [10, 20]});
            let font_size =  stripe_height*0.4*y_scale(stripe_width);
            if(d.label.length > 10 && d.label.length <= 22 ){
                font_size = stripe_height*0.35*y_scale(stripe_width);
            }else if( d.label.length > 22){
                font_size = stripe_height*0.31*y_scale(stripe_width);
            }
            return '<div' +
                ' style="width:'+ (stripe_width-8)  + 'px;"' +
                //' font-size:'+ font_size +'pt"' +
                ' class="' + stripe_class + '"' +
                '>'
                +  d.label
                + '</div>'});

    // adding value container:
    let value_cell = cell.append('div')
        .style('height', (cell_height - stripe_height) + "px")
        .attr("class", "col-sm-8")
        .style('width', stripe_width + "px")
        .append("xhtml:body")
        .style("background-color", "transparent")
        .html( function (d) {
            let font_size =  stripe_height*0.45;
            return '<div' +
                ' id="' + d.tag + '";' +
                ' style="width:'+ stripe_width  + 'px;' +
                ' height:' + stripe_height + 'px;"' +
                // ' font-size:'+ font_size +'px"' +
                ' class="' + value_class + '"' +
                '>'
                +  "L ----.-- "
                + '</div>'});

    // when all is done then return callback to say that all was done:
    callback(null);
}
