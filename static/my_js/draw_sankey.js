
function draw_sankey(sankey, svg, data, units, color_scale, ds_nodes, callback) {

    let path = sankey.link();

    let formatNumber = d3.format(",.0f"),    // zero decimal places
        format = function (d) {
            return formatNumber(d).replace(/,/g, ' ').replace(/\./, ',') + " " + units;
        },
        // color = d3.scale.category20();
        color = color_scale;

    //set up graph in same style as original example but empty
    graph = {"nodes": [], "links": [], "node_names": []};

    for(let i in data) {
        let d = data[i];
        graph.nodes.push({"name": d.source});
        graph.nodes.push({"name": d.target});
        graph.links.push({
            "source": d.source,
            "target": d.target,
            "value": +d.value,
            "timestamp": d.timestamp
        });
    }
    /*  data.forEach(function (d) {

       });*/

    // return only the distinct / unique nodes
    graph.nodes = d3.keys(d3.nest()
        .key(function (d) {
            return d.name;
        })
        .map(graph.nodes));

    graph.nodes.forEach(function (d, i) {
        graph.node_names[i] = d;
    });

    // loop through each link replacing the text with its index from node
    graph.links.forEach(function (d, i) {
        graph.links[i].source = graph.nodes.indexOf(graph.links[i].source);
        graph.links[i].target = graph.nodes.indexOf(graph.links[i].target);
    });

    //now loop through each nodes to make nodes an array of objects
    // rather than an array of strings
    graph.nodes.forEach(function (d, i) {
        graph.nodes[i] = {"name": d};
    });

    sankey
        .nodes(graph.nodes)
        .links(graph.links)
        .layout(32);

// add in the links
    var link = svg.append("g").selectAll(".link")
        .data(graph.links)
        .enter().append("path")
        .attr("class", "link")
        .attr("d", path)
        .style("stroke-width", function (d) {
            return Math.max(1, d.dy);
        })
        .sort(function (a, b) {
            return b.dy - a.dy;
        });

// add the link titles
    link.append("title")
        .text(function (d) {
            label = d.source.name + " → " +
                d.target.name + "\n" + format(d.value);

            let id_source = graph.node_names.indexOf(d.source.name);
            let id_target = graph.node_names.indexOf(d.target.name);
            let source_value = graph.nodes[id_source].value;
            let target_value = graph.nodes[id_target].value;
            if(source_value> target_value){
                percentage = target_value/source_value * 100;
            }
            else{
                percentage = source_value/target_value * 100;
            }
            label += ("    (" + percentage.toFixed(1) + " %)")

            if(d.timestamp !== undefined){
                label += ("\n" + d.timestamp);
            }
            return label ;
        });

// add in the nodes
    var node = svg.append("g").selectAll(".node")
        .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        })
        .call(d3.behavior.drag()
            .origin(function (d) {
                return d;
            })
            .on("dragstart", function () {
                this.parentNode.appendChild(this);
            })
            .on("drag", dragmove));

// add the rectangles for the nodes
    node.append("rect")
        .attr("height", function (d) {
            return d.dy;
        })
        .attr("width", sankey.nodeWidth())
        .style("fill", function (d) {
            // return d.color = color_scale(d.name.replace(/ .*/, ""));
            return d.color = color_scale(d.name);
        })
        .style("stroke", function (d) {
            return d3.rgb(d.color).darker(2);
        })
        .append("title")
        .text(function (d) {
            if(ds_nodes[d.name] === undefined){
                return d.name + "\n" + format(d.value);
            }else{
                return d.name + "\n" + format(d.value) + "\n" + ds_nodes[d.name];
            }
        });

// add in the title for the nodes
    node.append("text")
        .attr("x", -6)
        .attr("y", function (d) {
            return d.dy / 2;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .attr("transform", null)
        .text(function (d) {
            return d.name;
        })
        .filter(function (d) {
            return d.x < width / 2;
        })
        .attr("x", 6 + sankey.nodeWidth())
        .attr("text-anchor", "start");

    /*
      // the function for moving the nodes
      function dragmove(d) {
        d3.select(this).attr("transform",
            "translate(" + d.x + "," + (
                    d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
                ) + ")");
        sankey.relayout();
        link.attr("d", path);
      }
    }); */


// the function for moving the nodes
    function dragmove(d) {
        d3.select(this).attr("transform",
            "translate(" + (
                d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
            )
            + "," + (
                d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
            ) + ")");
        sankey.relayout();
        link.attr("d", path);
    }

// #   });

    if(callback === undefined){
        return sankey;
    }
    else{
        callback(sankey);
    }

}