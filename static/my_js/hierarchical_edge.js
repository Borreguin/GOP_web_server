function draw_hierarchical_edge(h, w){
    var diameter = h,
        radius = diameter / 2,
        innerRadius = radius - 120;

    var cluster = d3.cluster()
        .size([360, innerRadius]);

    var line = d3.radialLine()
        .curve(d3.curveBundle.beta(0.7))
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    var svg = d3.select("#grid_1").append("svg")
        .attr("width", w)
        .attr("height", diameter)
        .append("g")
        .attr("transform", "translate(" + w/2 + "," + radius + ")");

    var link = svg.append("g").selectAll(".link"),
        // node = svg.append("g").selectAll(".node"),
        group = svg.append("g").selectAll(".group"),
        arc_group = svg.append("g").selectAll(".arc_group");

    d3.json("/static/flare.json", function(error, classes) {
      if (error) throw error;

      var root = packageHierarchy(classes)
          .sum(function(d) { return d.value; });

      cluster(root);

      test = root.leaves();
      test2 = root["children"];


      link = link
        .data(packageImports(root.leaves()))
        .enter().append("path")
          .each(function(d) { d.source = d[0], d.target = d[d.length - 1]; })
          .attr("class", "link")
          .attr("id", function(d, i){
            return nombre_link_unico(d[0].data.name);
          })
          .attr("d", line)
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


      var arc = d3.arc()
        .innerRadius(function(d){return 2*d.y+5;})
        .outerRadius(function(d){return 2*d.y+10;})
        .startAngle(function(d){return (d.children[0].x-1)*(Math.PI/180); }) //converting from degs to radians
        .endAngle(function(d){ return (d.children[d.children.length - 1].x + 1)*(Math.PI/180)} ); //just radians



      arc_group = arc_group
        .data(root["children"])
        .enter().append("path")
          .attr("d", arc)
          //.style("fill", "#990000");
          .style("fill", "blue");
          //.style("stroke", "orange");
          //.attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (2*d.y + 16) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); });

          // #-> id
        d3.select("#Santa_Rosa-Totoras--1")
            .style("stroke", "gray");
         // . -> class
        d3.select("#Baba-Santo_Domingo--1")
            .style("stroke", "gray");

        d3.select("#Santa_Rosa-Totoras--2")
            .style("stroke", "#800055");
            //.style("stroke-width", "0.5px");

        d3.select("#Chorrillos-Quevedo--1")
            .style("stroke", "orange");

        d3.select("#Chorrillos-Quevedo--2")
            .style("stroke", "orange");

        d3.select("#Esclusas-Sopladora--1")
            .style("stroke", "red");

        d3.select("#Molino-Pascuales--1")
            .style("stroke", "green");
        //	.style("stroke-width", "0.5px");

        d3.selectAll(".link").style("stroke", "orange");

        let aux = d3.select("El Inga#Pomasqui--1");
        console.log(aux);

    });

    function valid_str(label){
        label = label.replace(" ", "_");
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


    function selected_link(d, i){
        let source_group = valid_str(d.source.parent.data.key);
        let target_group = valid_str(d.target.parent.data.key);

        d3.select(this)
              .attr("class", "link_selected");

        d3.selectAll("#gp_" + source_group + ", #gp_" + target_group)
                .attr("class", "group_selected");
    }

    function normal_link(d, i){
        let source_group = valid_str(d.source.parent.data.key);
        let target_group = valid_str(d.target.parent.data.key);

        d3.select(this)
              .attr("class", "link");

        d3.selectAll("#gp_" + source_group + ", #gp_" + target_group)
                .attr("class", "group");

    }


    function selected_group(d, i){
        let children_group = d["data"]["children"];
        let group = valid_str(d.data.key);

        d3.select("#gp_" + group)
                .attr("class", "group_selected");

        children_group.forEach(function(e){
            d3.select("#" + nombre_link_unico(e.name))
                .attr("class", "link_selected");
        });
    }

    function normal_group(d, i){
        let children_group = d["data"]["children"];
        let group = valid_str(d.data.key);

        d3.select("#gp_" + group)
                .attr("class", "group");

        children_group.forEach(function(e){
            d3.select("#" + nombre_link_unico(e.name))
                .attr("class", "link");
        });

    }

}