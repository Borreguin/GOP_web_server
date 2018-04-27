let margin = {
        top: 5,
        right: 5,
        bottom: 5,
        left: 5
};

let bar_size = 160;
let w = $(document).width();
let h = $(document).height();
let height =  Math.max(Math.min(h, 800), 300) - margin.top - margin.bottom - bar_size;
let width = Math.max(Math.min(w, 1200), 500) - margin.left - margin.right;




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
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

	// icon size and cell size
	let icon_width = w_panel*0.30;
    let cell_height = h_panel/n_data;

    //let gallery = d3.select(to_plot).append('div');

    let container = gallery.selectAll('.container_panel')
        .data(data_panel, function(d) { return d.id; });

    let cell = container.enter().append('div')
        .attr('class', 'container_panel')
        .attr('height', cell_height)
        .attr('width', w_panel);

    // adding icons:
    let icons = cell.append('div')
        .attr("class", "rs_icon")
        .attr('height', cell_height);

    // adding panel display
    let val_cell = cell.append('div')
        .attr("class", "col-sm-8")
        .append('svg')
        .attr('height', cell_height)
        .attr('width', w_panel - icon_width - 10)
        .append('rect')
        .attr('height', cell_height)
        .attr('width', w_panel - icon_width - 10);

    icons.append('img')
        .attr('class', 'img')
        .style("height", cell_height + "px")
        .attr('src', function(d) { return d.icon; });


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