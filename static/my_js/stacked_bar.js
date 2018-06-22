let blue_scale_9 = color_scale(
    ["#000046", "#0033CC", "#0066FF", "#6399FF", "#66CCFF", "#99FFFF", "#DCFFFF", "#6633DF", "#9999FF"  ]);

let orange_scale_8 = color_scale(
    ["#FF5500", "#FF9900", "#FFCC00", "#FFCC66",  "#FFFF99",  "#FFFFCC",  "#CC9900" , "#CCFF33" ]);


let colour_bar;
let width_bar, height_bar, wide_bar;
let bar_container;
let center_bar;
let x_offset_val;
let svg_container;
let bar_middle = {};

let bar_data = [
    {"id":0, "label" : "Agoyán", "value": "40000 MWh", "percentage": 0.20},
	{"id":1, "label" : "Paute", "value": "200 MWh", "percentage": 0.20},
	{"id":2, "label" : "Coca Codo", "value": "100 MWh", "percentage": 0.01},
    {"id":3, "label" : "Marcel Laniado", "value": "100 MWh", "percentage": 0.10},
    {"id":4, "label" : "San Francisco", "value": "100 MWh", "percentage": 0.10},
	{"id":5, "label" : "Otras Hidro", "value": "300 MWh", "percentage": 0.15},
    {"id":6, "label" : "item 6", "value": "100 MWh", "percentage": 0.05},
	{"id":7, "label" : "item 7", "value": "100 MWh", "percentage": 0.10},
    {"id":8, "label" : "item 8", "value": "100 MWh", "percentage": 0.03},
    {"id":9, "label" : "item 9", "value": "100 MWh", "percentage": 0.02}

];


let to_plot_bar = "#viz";



function draw_stk_bar(to_plot, data_to_plot, w_bar_size, h_bar_size, x_borde, colors){
	to_plot_bar = to_plot;
    width_bar = w_bar_size;
    height_bar = h_bar_size;
	colour_bar = colors;
	wide_bar = width_bar*0.10;
	bar_data = data_to_plot;
	y_offset_val = h_bar_size*0.02;
    x_offset_val = x_borde;
	center_bar = (width_bar + 2*Math.abs(x_borde))/2;
	bar_middle = {};

    // cleaning the space to work with
    d3.select(to_plot).select("svg").remove();
    d3.select(to_plot).select("img").remove();

    svg_container = d3.select(to_plot)
        .append("svg")
        .attr("width", width_bar + 2*x_offset_val)
        .attr("height", height_bar + 2.5*y_offset_val);

    bar_container = svg_container.selectAll('.container_bar')
        .data(bar_data, function(d) { return d.id; });
   
    let y_scale = scaleLinear({domain:[0, 1], range:[0, height_bar-y_offset_val]});
	
	
    let stacked_value = height_bar + y_offset_val;
	
    let cells = bar_container.enter()
		.append("g")
		.append('rect')
        .attr('class', 'container_bar')
        .attr("x", center_bar - wide_bar/2)
        .attr("y", function(d){
            stacked_value = stacked_value - y_scale(d.percentage);
			bar_middle[d.id] = stacked_value + y_scale(d.percentage)/2;
            return stacked_value;
            })
        .attr("width", wide_bar)
        .attr("height", function(d){
            return y_scale(d.percentage) ;
        })
        .attr("stroke", colour_bar(0))
        .attr("fill", function(d){
            let aux1 = colour_bar(d.id);
            return colour_bar(d.id);
        });
		
	return cells;
}

function add_tooltips(cells, myTool){
	
	cells
	.on("mouseover", function(d){  //Mouse event
		let ref = d3.select(this);
		
		// bring to front:
		ref.each(function(){
			this.parentNode.appendChild(this);});
		
		ref
			.transition()
			.duration(100)
			.attr("stroke-width", 4)
			.attr("stroke", "orange");
		
		myTool
			.transition()  //Opacity transition when the tooltip appears
			.duration(500)
			.style("opacity", "1")                           
			.style("display", "block");  //The tooltip appears
			
		let ans = getAbsoluteXY(this);
        //let dx = parseFloat(ref.attr("x")) +  parseFloat(ref.attr("width")) + 5;
		//let dy = parseFloat(ref.attr("y")) - 20;
		let dx = ans.x +  wide_bar*1.5;
		let dy = ans.y - 24;

		myTool
		  .html("<div id='thumbnail'><span>" + d.label + "</span> </br>" + 
				"<span>" + d.value + "</span> </br>" +  
				"<span>" + Math.round(d.percentage*100,2) + " %" + "</span> </br>" + "</div>")
		  .style("left", (dx + "px"))   
		  .style("top", (dy + "px"));
		  
	})
	.on("mouseout", function(d){  //Mouse event
		d3.select(this)
		.transition()
		.duration(100)
		//.style("cursor", "normal")
		.attr("stroke-width", 1)
		.attr("stroke", colour_bar(0))
		myTool
			.transition()  //Opacity transition when the tooltip disappears
			.duration(500)
			.style("opacity", "0")            
			.style("display", "none")  //The tooltip disappears
	});
}


function add_labels(cells){


	let y_scale = scaleLinear({domain:[0, 1], range:[0, height_bar]});
	let dx = 0, dy = 0;
	let y_left = {};
	let y_right = {};
	let labels = svg_container.selectAll("g")
		.append("g")
		.attr("class", "my_container_label")
		.attr("transform", function(d){ 
			// ----- Defining x --------
			if(is_even(d.id)){dx = center_bar + 1.2*wide_bar;}
			else{dx = center_bar - 1.2*wide_bar; }
			
			// ----- Defining y --------
			if(d.id <= 1){ dy = (bar_middle[d.id] + height_bar)*0.5}
			else{
				let lim = 0;
				if(is_even(d.id)){lim=y_right[d.id-2] - 75}
				else{lim=y_left[d.id-2] - 75}

                if(bar_middle[d.id] <= lim ) {
                    for (let i = 0; i <= 7; i++) {
                        if (bar_middle[d.id] + i * 10 < lim) {
                            dy = bar_middle[d.id] + i * 10;
                        } else {
                            break;
                        }
                    }
                }else{
				    for (let i = 0; i <= 7; i++) {
				        if(lim < 100){
				            dy = bar_middle[d.id]*0.5;
				            break;
                        }
                        if (bar_middle[d.id] - i * 10 > lim ) {
                            dy = bar_middle[d.id] - i * 10;
                        } else {
                            break;
                        }
                    }
                }
			}
			if(is_even(d.id)){y_right[d.id] = dy;}
			else{y_left[d.id] = dy;}
			return "translate(" + dx + "," + dy + ")";
		})
		.style("text-anchor", function(d){
			if(is_even(d.id)){return "start";}
			else{return "end";}
		});
		
	labels
		.append("text")
		.attr("class", "my_label")
		.text(function(d){ 
			d.size = d.label.length;
			return d.label;
		});
		
	labels
		.append("text")
		.attr("class", "my_label")
		.attr("dy", "1em")
		.text(function(d){ 
			if(d.size < d.value.length){
				d.size = d.value.length
			}
			return d.value;
		});
		
	labels
		.append("text")
		.attr("class", "my_label")
		.attr("dy", "2em")
		.text(function(d){ 
			let str = "( " + Math.round(d.percentage*100,1) + " %)";
			if(d.size < str.length){
				d.size = str.length
			}
			return str;
		});
		
	let l_scale = scaleLinear({domain:[7, 18], range:[80, 140]});
	
	labels
		.append("rect")
		.attr("height", 55)
		.attr("width", function(d){ return l_scale(d.size);})
		.attr("class", "my_ballon")
		.attr("rx", 8)
		.attr("ry", 8)
		.attr("transform", function(d){
			let cy = "," + (-16) + ")";
			let cx = "-5";
			if(!is_even(d.id)){
				cx = - l_scale(d.size) + 5;
			}
			return "translate(" + cx + cy;});
	
	for(i in bar_middle){
		let y2 = bar_middle[i];
		let y1, x2;
		if(is_even(parseInt(i))){
			x1 = center_bar + 1.18*wide_bar;
			y1 = y_right[i];
			x2 = center_bar + wide_bar/2;
		} 
		else{
			x1 = center_bar - 1.18*wide_bar;
			y1 = y_left[i];
			x2 = center_bar - wide_bar/2;
		}
			
		svg_container
			.append("line")
			.attr("x1", x1)
			.attr("y1", y1 - 16)
			.attr("x2", x2)
			.attr("y2", y2)
			.attr("opacity", 0.3)
			.attr("stroke-width", 1.5)
			.attr("stroke-dasharray", '3')
			.attr("stroke", "black");
	
	}
	
}

function is_even(n){
	return (n === 0 || !! (n && !(n%2)));
}

function getAbsoluteXY(element) {
   var viewportElement = document.documentElement;
   var box = element.getBoundingClientRect();
   var scrollLeft = viewportElement.scrollLeft;
   var scrollTop = viewportElement.scrollTop;
   var x = box.left + scrollLeft;
   var y = box.top + scrollTop;
   return {"x": x, "y": y}
}

/* Example */
// cells = draw_stk_bar(bar_data, to_plot_bar, blue_scale_9);
// add_tooltips(cells, myTool_right);
// add_labels(cells);

