// let scale_car = d3.scaleLinear().domain([88.8, 165]).range([2,7]);
// let scale_car = d3.scaleLinear().domain([247, 494]).range([2,7]);

let arc_colors = {
    "500 kV": "#bb4437",
    "230 kV": "#2d49bb",
    "138 kV": "#ff8c29"
};

format_w_spaces = function (d) {
    return formatNumber(d).replace(/,/g, ' ').replace(/\./, ',');
};

formatNumber = d3.format(",.0f");    // zero decimal places



function draw_hierarchical_edge(div_to_graph, grah_data){

    d3.select("#" + div_to_graph).selectAll("*").remove();
    let h = document.getElementById(div_to_graph).offsetHeight;
    let w = document.getElementById(div_to_graph).offsetWidth;
    let classes = grah_data.data;
    /*let scale_car = d3.scaleLinear()
        .domain([grah_data.settings["min"], grah_data.settings["max"]])
        .range([2,7]);*/

    const x = d3.scaleTime().range([0, w]);
    const y = d3.scaleLinear().range([h, 0]);

    var diameter = h,
        radius = diameter / 2,
        innerRadius = radius - 200;

    var cluster = d3.cluster()
        .size([360, innerRadius]);

    var line = d3.radialLine()
        .curve(d3.curveBundle.beta(0.7))
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    var svg = d3.select("#" + div_to_graph).append("svg")
        .attr("width", w)
        .attr("height", diameter)
        .append("g")
        .attr("transform", "translate(" + w/2 + "," + radius + ")");

    var link = svg.append("g").selectAll(".link"),
        // node = svg.append("g").selectAll(".node"),
        group = svg.append("g").selectAll(".group"),
        arc_group = svg.append("g").selectAll(".arc_group");

    create_hierarchical_edge(classes);

    function create_hierarchical_edge(classes){
    //d3.json("/static/flare.json", function(error, classes) {
    //  if (error) throw error;

      var root = packageHierarchy(classes)
          .sum(function(d) { return d.value; });

      cluster(root);


      link = link
        .data(packageImports(root.leaves()))
        .enter().append("path")
          .each(function(d) { d.source = d[0]; d.target = d[d.length - 1]; })
          .attr("class", "link")
          .attr("id", function(d, i){
            return nombre_link_unico(d[0].data.name);
          })
          .attr("d", line)
          .style("stroke-width", function (d) {
              let ind_scale = d3.scaleLinear()
                  .domain([d[0].data.value["Lim_Termico"]*0.01, d[0].data.value["Lim_MaxOperacion"]])
                  .range([2,7]);

              return ind_scale(d[0].data.value["current_value"])+ "px";
          })
          .style("stroke", function (d) {
              return colorear_link(d[0].data);
          })
          /*.style("stroke-dasharray", function (d) {
              let dif = d[0].data.value["dif"];
              if(dif > d[0].data.value["Lim_Termico"]*0.20){
                    return 4;
              }else{
                    return 0;
              }

          })*/
          .on("mouseover", selected_link)
          .on("mouseout", normal_link);

     /* node = node
        .data(root.leaves())
        .enter().append("text")
          .attr("class", "node")
          .attr("dy", "0.31em")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
          .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          //.text(function(d) { return d.data.key; });
          .text(function(d) { return '.'; });*/

       group = group
        .data(root["children"])
        .enter().append("text")
          .attr("class", "group")
          .attr("dy", "0.31em")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (2*d.y + 16) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
          .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
          .attr("id", function(d){ return "gp_" + valid_str(d.data.key);})
          .text(function(d) { return d.data.key; })
          .on("mouseover", selected_group)
          .on("mouseout", normal_group);
          //.on("mousemove", display_values);


      var arc = d3.arc()
        .innerRadius(function(d){return 2*d.y+5;})
        .outerRadius(function(d){return 2*d.y+10;})
        .startAngle(function(d){return (d.children[0].x-1)*(Math.PI/180); }) //converting from degs to radians
        .endAngle(function(d){ return (d.children[d.children.length - 1].x + 1)*(Math.PI/180)} ); //just radians


      arc_group = arc_group
        .data(root["children"])
            .enter()
            .append("path")
            .attr("d", arc)
            .style("fill", function (d) {
                let v = d.children[0].data.value["Voltaje"];
                return arc_colors[v];
              });


    }



    // Lazily construct the package hierarchy from class names.
    function packageHierarchy(classes) {
      var map = {};

      function find(name, data) {
        var node = map[name], i;
        if (!node) {
          node = map[name] = data || {name: name, children: []};
          if (name.length) {
            node.parent = find(name.substring(0, i = name.lastIndexOf("#")));
            node.parent.children.push(node);
            node.key = name.substring(i + 1);
          }
        }
        return node;
      }

      classes.forEach(function(d) {
        find(d.name, d);
      });

      return d3.hierarchy(map[""]);
    }

    // Return a list of imports for the given array of nodes.
    function packageImports(nodes) {
      var map = {},
          imports = [];

      // Compute a map from name to node.
      nodes.forEach(function(d) {
        map[d.data.name] = d;
      });

      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.data.imports) d.data.imports.forEach(function(i) {
          imports.push(map[d.data.name].path(map[i]));
        });
      });

      return imports;
    }


    function selected_link(d) {
        let source_group = valid_str(d.source.parent.data.key);
        let target_group = valid_str(d.target.parent.data.key);

        let x_p = d3.event.pageX;
        let y_p = d3.event.pageY;

        d3.select(this)
            .attr("class", "link_selected")
            .moveToFront();


        d3.selectAll("#gp_" + source_group + ", #gp_" + target_group)
            .attr("class", "group_selected");

        div.style("display", "inline");

        let values = d[0].data.value;

        div.transition()
         .duration(200)
         .style("opacity", .95);
       div.html( "<strong>" +  values["Linea"] + "</strong>"
           + "<br/> V. actual: <strong>" + format_w_spaces(values["current_value"])  + " MVA ( "
           + format_w_spaces(values["current_value"]/values["Lim_Termico"]*100) + " %)</strong>"
           + "<br/> Capacidad:   " + values["Lim_Termico"]  + " MVA"
           + "<br/><br/>" + values["timestamp"])
         .style("left", x_p + "px")
         .style("top", y_p + "px");


        console.log("select", d[0].data.value);
    }



    function normal_link(d, i){
        let source_group = valid_str(d.source.parent.data.key);
        let target_group = valid_str(d.target.parent.data.key);

        d3.select(this)
              .attr("class", "link");

        d3.selectAll("#gp_" + source_group + ", #gp_" + target_group)
                .attr("class", "group");
        div.style("display", "none");
    }


    function selected_group(d, i){

        let children_group = d["data"]["children"];
        let group = valid_str(d.data.key);

        d3.selectAll("#gp_" + group)
                .attr("class", "group_selected")
                .moveToFront();

        children_group.forEach(function(e){
            d3.selectAll("#" + nombre_link_unico(e.name))
                .attr("class", "link_selected")
                .moveToFront();

            let grp = valid_str(e.name).split("-");

            d3.selectAll("#gp_" + grp[0])
                .attr("class", "group_selected")
                .moveToFront();

            d3.selectAll("#gp_" + grp[1])
                .attr("class", "group_selected")
                .moveToFront();
        });
    }

    function normal_group(d, i){
        let children_group = d["data"]["children"];
        let group = valid_str(d.data.key);

        d3.selectAll("#gp_" + group)
                .attr("class", "group");

        children_group.forEach(function(e){
            d3.select("#" + nombre_link_unico(e.name))
                .attr("class", "link");

            let grp = valid_str(e.name).split("-");

            d3.selectAll("#gp_" + grp[0])
                .attr("class", "group")
                .moveToFront();


            d3.selectAll("#gp_" + grp[1])
                .attr("class", "group")
                .moveToFront();
        });

    }

    d3.selection.prototype.moveToFront = function() {
        return this.each(function(){
        this.parentNode.appendChild(this);
        });
    };

    function colorear_link(d){
        /*console.log(d.value.Linea, d.value);*/
        if(d.value["current_value"] < 2) {return "gray"}
        if(d.value["mean"]==null || d.value["quality"]==="TE"){return "#ee14cf"}
        if(d.value["quality"]==="ME"){return "#5da0ee"}
        var scale_color = d3.scaleLinear()
            .domain([d.value["Lim_Termico"]*0.01,
                d.value["Lim_Termico"]*0.5,
                d.value["Lim_Termico"]*1.1,
                d.value["Lim_MaxOperacion"]])
            .range([
                '#26ab97',
                '#309645',
                '#ff5d05',
                 '#ff1f40']).interpolate(d3.interpolateHcl);

        return scale_color(d.value["current_value"]);
    }
    function opacity_value(d){
            var scale_opacity = d3.scaleLinear()
            .domain([d.value["Lim_Termico"]*0.01, d.value["Lim_Termico"]])
            .range([0.3, 1]);

        return scale_opacity(d.value["current_value"]);
    }
}

function valid_str(label){
    label = label.replace(/\s/g, "_");
    label = label.replace(' ', "_");
    label = label.replace("#", "-");
    return label;
}

function nombre_link_unico(label){
    label = valid_str(label);
    let aux = label.split("--");
    let res = aux[0].split("-");
    if(res[0] < res[1]){
        return res[0] + "-" + res[1] + "--" + aux[1];
    }else{
        return res[1] + "-" + res[0] + "--" + aux[1];
    }

}

