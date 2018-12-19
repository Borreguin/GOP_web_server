
function graph_FOR(div, graph_data, config) {
    n = config.n;
    let voltaje = config.voltaje;

    /*data = [
        {"area": "central ", "value": 18000},
        {"area": "Riverside ", "value": 17000},
        {"area": "Picton ", "value": 80000},
        {"area": "Everton ", "value": 55000},
        {"area": "Kensington ", "value": 100000},
        {"area": "Kirkdale", "value": 50000}
    ];*/
    data = [];

    //console.log(graph_data);
    for(let i in graph_data){
        let el = graph_data[i];
        if(voltaje === el.Voltaje){
            let lab = el["Línea"].replace(voltaje + " kV", "");
            let val = el["FOR"];
            data.push({"area":lab, "value": val});
        }
    }
    graph_bar(div, data);
    /* let x_n =[...Array(lab.length).keys()];
    let trace = {
        type: 'bar',
        x:val.reverse(),
        y:x_n,
        orientation:'h'
    };
    let layout = {
        paper_bgcolor:'black',
        plot_bgcolor: 'black',
        font: {
            size: 12,
            color: '#ffffff'
            },
        yaxis: {
            side: 'right',
            // title: "Idea",
            tickmode: "array",
            tickvals: x_n,
            ticktext: lab.reverse()
        },
        margin: {
            l: 10,
            r: 200,
            b: 50,
            t: 50,
            pad: 4
        }

    };

    Plotly.newPlot(div, [trace], layout);  */
}

function graph_bar(div, data) {

    let h = document.getElementById(div).offsetHeight;
    let w = document.getElementById(div).offsetWidth;
    var svg = d3.select("#" + div)
        .append("svg")
        .attr("height", h)
        .attr("width", w);

    var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = w - margin.left - margin.right,
    height = h - margin.top - margin.bottom;

    var tooltip = d3.select("body").append("div").attr("class", "toolTip");

    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleBand().range([height, 0]);

    var g = svg.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

/*d3.json("data.json", function(error, data) {
  	if (error) throw error;*/

  	data.sort(function(a, b) { return a.value - b.value; });

    let x_max = d3.max(data, function(d) { return d.value; });
    let y_max = data.map(function(d) { return d.area; });

  	x.domain([0, x_max]);
    y.domain(y_max).padding(0.1);

    g.append("g")
        .attr("class", "x axis")
       	.attr("transform", "translate(0," + height + ")")
      	.call(d3.axisBottom(x).ticks(5).tickFormat(function(d) { return parseInt(d / 1000); }).tickSizeInner([-height]));

    g.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y));

    g.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("height", y.bandwidth())
        .attr("y", function(d) { return y(d.area); })
        .attr("width", function(d) { return x(d.value); })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.area) + "<br>" + (d.value));
        })
    		.on("mouseout", function(d){ tooltip.style("display", "none");});
//})

}
