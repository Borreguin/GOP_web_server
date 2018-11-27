let time_minutes = 6.5;
        let ct_date = new Date(Date.parse(date + " " + hour));
        // let today_date = new Date();
        let style = "black_style";
        let styles = {default: "#203864", white_style: "white", black_style: "black"};
        let init_ap = true, upd_w = 0;
        let url_graph;
        let graph_data_global;
        let date_arg;
        let hour_arg;


        function updating_all() {
            update_time_with("fecha_actual",ct_date);

            date_arg = ct_date.getFullYear() + "-" + (ct_date.getMonth() + 1) + "-" + ct_date.getDate();
            hour_arg = ct_date.toLocaleTimeString('it-IT');
            url_graph = '/grafica_pronostico/' + description + "/" +  date_arg + "/" + hour_arg + "/" + style;

            queue()
                .defer(d3.json, url_graph)
                .await(update_graph);

            // increase X minutes each time:
            ct_date = add_time(ct_date, time_minutes);
            setTimeout(updating_all, time_minutes*1000*60);
        }

        function update_graph(error, graph_data){
            graph_data_global = graph_data;
            let panel_info = graph_data.panel_info;
            let new_layout = adapt_layout(graph_data.layout);
            let new_values = adapt_values(graph_data.data);
            Plotly.react("div_demanda", graph_data.data, new_layout);
            if(init_ap){add_sytles(); init_ap=false;}

        }
        function new_graph(error, graph_data) {
            let new_layout = adapt_layout(graph_data.layout);
            let new_values = adapt_values(graph_data.data);
            Plotly.newPlot("div_demanda", new_values, new_layout);
            add_sytles();
        }

        function adapt_layout(layout){

            layout.showlegend = true;
            layout.legend= {"orientation": "h", x: -0.05, y: 1.1};
            layout.font.size = 17;
            //layout.xaxis.dtick=4000 * 60 * 60;
            layout.xaxis.tickformat = '%H';
            layout.yaxis2.range= [-210, 210];
            //layout.yaxis.gridcolor = '#6c696d';
            //layout.yaxis2.gridcolor = '#6c696d';
            //layout.xaxis.gridcolor = '#6c696d';
            return layout;

        }

        function adapt_values(values) {
            //console.log(values);
            for(let id in values){
                vals = values[id];
                if(vals["name"]=== "Desv. demanda programada"){
                    old_y = vals.y;
                    new_y = [];
                    old_y.forEach(function (e) {
                        new_y.push(parseInt(e));
                    });
                    values[id].text = new_y;
                    values[id].y = new_y;
                    values[id].textfont ={
                        'family': 'Verdana',
                        'size' : 18,
                        'color' :'#419539'
                    };
                }
                if(vals["name"]=== "Desviación estándar"){
                    values[id] = {};
                }
                if(vals["name"] === "Despacho programado"){
                    values[id]["name"] = "Programado"
                }
                if(vals["name"] === "Demanda real"){
                    values[id]["name"] = "Real"
                }
                if(vals["name"] === "Demanda esperada"){
                    values[id]["name"] = "Proyectada"
                }
                if(vals["name"] === "Desv. demanda programada"){
                    values[id]["name"] = "Diferencia"
                }

            }
            return values;
        }


        function add_sytles(){
            let menu_container = d3.select(".modebar");
            for(id in styles){
                menu_container
                    .append("div")
                    .attr("id", id)
		            .attr("class", "modebar-group")
                    .style("background-color", styles[id])
                    .style("margin-left", "0px")
                    .style("font-size", "8pt")
                    .html('<a rel="tooltip" class="modebar-btn" data-title="Select style color" > sty' +
                           '</a>')
                    .on("click", function() {
                        style = d3.select(this).attr("id");
                        url = "/get_graph_layout/" + style;
                        d3.json(url, function (layout_style) {
                            graph_data_global.layout = layout_style;
                            new_graph(null, graph_data_global);
                        });
                    });
            }
        }


        updating_all();

    async function loading(ini, fin, callback){

        let msg = "Espere por favor: <br/>";
        for(let i=ini; i<=fin; i++){
            msg += "|";
            if(d3.select("#title_result").text() === "Procesando..."){
                d3.select("#msg_result")
                    .html(msg + "<br/>" + i + "%");
            }
            await sleep(500);
        }
        if(callback === undefined){
            return null
        }else{
            callback(null);
        }
    }
