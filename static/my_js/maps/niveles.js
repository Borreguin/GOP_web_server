let general_range = [500, 4200]; //"#bcbddc"
let color_band = ['rgba(255, 170, 0, 0.8)',
    "#006080",
    "#31a354",
    "#969696",
    "#fdae6b",
    "#00b3b3",
    "#999900",
    "#5a7c91",
    "#fd8d3c",
    "#a1d99b",
    "#c262e1",
    "#5cb353"];

function nivel_global(){

    last_time = time_last_30_min();
    let stamp_time = to_yyyy_mm_dd_hh_mm_ss(last_time)

    queue()
          .defer(draw_ecuador_in_world, 'main_grid')
          .defer(d3.json, '/cal/demanda_empresas/'+ stamp_time + "&7")
          .defer(d3.json, '/cal/demanda_nacional_desde_sivo')
          .defer(d3.json, '/cal/informacion_sankey_generacion_demanda')
          .defer(d3.json, '/cal/maxima_demanda_nacional')
          .await(function(error, ec_map, js_barras, js_dm, js_sankey, js_max){
                if(error) throw error;
                plot_sankey(error, js_sankey, "Demanda Nacional");
                update_barras_demanda(error, js_barras);
                let mx_date = js_max[0]["Fecha"];
                queue()
                    .defer(d3.json, '/cal/demanda_nacional_desde_sivo/' + mx_date)
                    .await(function (error, js_dm_hist) {
                        let dats = [js_dm_hist, js_dm];
                        let labels = [mx_date + ": Histórico", "Demanda actual" ];
                        let ls_color = ['rgba(255, 255, 255, 0.2)', 'rgba(255, 170, 0, 0.8)'];
                        update_trend(error, dats, labels, ls_color);
                        plot_maxima_demanda(error, js_max)
                    });

           });
}

function nivel_regional() {

    last_time = time_last_30_min();
    let stamp_time = to_yyyy_mm_dd_hh_mm_ss(last_time)

    queue()
          .defer(draw_ecuador_only, 'main_grid')
          .defer(d3.json, '/cal/tendencia_demanda_nacional_por_regiones')
          .defer(d3.json, '/cal/informacion_sankey_generacion_demanda_regional/' + stamp_time)
          .defer(d3.json, '/cal/demanda_regiones/' + stamp_time)
          .await(function(error, ec_map, js_dm_reg, js_sankey, js_barras){
                if(error) throw error;
                ec_map = pintar_regiones_del_ecuador(ec_map);
                dw_sankey = plot_sankey(error, js_sankey, "Demanda Nacional");
                let colors = {"Sierra": "#0e283b" , "Costa": "rgba(100, 10, 10, 1)", "Oriente": "rgba(0, 74, 86, 1)"};
                st1 = update_stacked_trend(error, js_dm_reg, colors, "DEMANDA NACIONAL [MW]");
                st2 = update_colored_bars(error, js_barras, colors);
                if(ec_map !== undefined && dw_sankey !== undefined && st1 !== undefined && st2 != undefined){
                    mover_regiones();
                    stop_all();
                }
           });

}


function nivel_empresarial() {

    last_time = time_last_30_min();
    let stamp_time = to_yyyy_mm_dd_hh_mm_ss(last_time)

    queue()
          .defer(draw_ecuador_only, 'main_grid')
          .defer(d3.json, '/cal/tendencia_demanda_nacional_por_nivel_empresarial')
          .defer(d3.json, '/cal/informacion_sankey_generacion_demanda_nivel_empresarial/' + stamp_time)
          .defer(d3.json, '/cal/demanda_por_nivel_empresarial/' + stamp_time)
          .await(function(error, ec_map, js_dm_emp, js_sankey, js_barras){
                if(error) throw error;
                ec_map = pintar_por_empresas(ec_map);
                dw_sankey = plot_sankey(error, js_sankey);
                let colors = {"CNEL": "#64467d", "Empresas Eléctricas": "#4e93c5"};
                st1 = update_stacked_trend(error, js_dm_emp, colors, "DEMANDA NACIONAL [MW]");
                st2 = update_colored_bars(error, js_barras, colors);
                if(ec_map != undefined && dw_sankey != undefined && st1 != undefined && st2 != undefined){
                    mover_regiones();
                    stop_all();
                }

           });

}


function nivel_provincial() {

    last_time = time_last_30_min();
    let stamp_time = to_yyyy_mm_dd_hh_mm_ss(last_time)


    queue()
          .defer(draw_ecuador_only, 'main_grid')
          .await(function(error, ec_map){
                if(error) throw error;
                // para actualizar datos generales:
                let colors = {"Sierra": "#0e283b" , "Costa": "rgba(100, 10, 10, 1)", "Oriente": "rgba(0, 74, 86, 1)"};
                seleccionar_mapa("Pichincha");
                pintar_regiones(ec_map, ["Pichincha"], "rgba(255, 150, 0, 1)");

           });

}





//------------------------------------------------------------------------------------------------------
//  FUNCIONES AUXILIARES:

function plot_maxima_demanda(error, graph_data) {

    let data = graph_data[0];
    let generacion_maxima = data["DeePerdidas"];
    let demanda_maxima = data["MW_Demanda"];
    let layout = {
        shapes: [
        {
            type: 'line',
            xref: 'paper',
            x0: 0,
            y0: generacion_maxima,
            x1: 1,
            y1: generacion_maxima,
            line:{
                color: '#4a89bf',
                width: 2,
                dash:'dot'
            }
        }]
    };

    let today = new Date();
    today = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + data["Hora"];

    let trace1 = {
          x: [today],
          y: [generacion_maxima],
          mode: 'lines+markers+text',
          name: data["Fecha"],
          text: ['máxima demanda histórica'],
          textposition: 'top',
          type: 'scatter',
          marker:{color: '#4a89bf'},
          textfont: {size: 12}
    };
    Plotly.relayout('grid_1', layout);
    Plotly.addTraces('grid_1', [trace1]);
}



function update_barras_demanda(error, graph_data) {

    let y = Object.keys(graph_data["current_value"]).reverse();
    y = y.map(function (value, idx) { return value.toUpperCase(); });
    let x = Object.values(graph_data["current_value"]).reverse();

    let x_d = Object.values(graph_data["dif"]).reverse();
    let x_p = Object.values(graph_data["percentage"]).reverse();
    let text_p = [], text_d =[];
    for(let ix in x_d){
        a_t = "max: " +  format_w_spaces(x_d[ix] + x[ix]) + " MW";
        text_p.push(a_t);
        text_d.push(x[ix] + " MW");
    }

    let data = [
        {
            x: x, y: y, type: 'bar', orientation: 'h',
            // text: text_d,
            textposition: 'auto', name: "Empresa",
            hoverinfo: 'none',
            marker: {
                color: 'rgba(255, 170, 0, 0.9)',
                opacity: 1
            }
        },
        {
            x: x_d, y: y, type: 'bar',
            orientation: 'h',
            text: text_p,
            // textposition: 'auto',
            align:'right',
            hoverinfo: 'text',
            marker: {
                color: 'rgba(64, 64, 64, 0.8)',
                opacity: 0.8
            }
        }
    ];

    let layout = get_layout_bar();
    let dist = Math.max.apply(null, x) + Math.max.apply(null, x_d) + 100;
    for(let i = 0 ; i < y.length ; i++){
        let annotation = {
            xref: 'x1',
            yref: 'y1',
            x: dist,
            y: y[i],
            text: '<b>'+ x_p[i] + '</b>',
            align: 'left',
            font: {
              //family: 'Arial',
              size: 12,
              color: 'white',

            },
             showarrow: false,
            };
            layout.annotations.push(annotation);

            /*if(x[i] < 0.15*dist){
                ds_x = 0.15*dist;
            }else{
                ds_x = x[i];
            }*/

            annotation = {
            xref: 'x1',
            yref: 'y1',
            x: dist*0.05,
            y: y[i],
            text: '<b>'+ format_w_spaces(x[i]) + '</b>',
            align: 'left',
            font: {
              //family: 'Arial',
              size: 12,
              color: 'rgb(0, 0, 0)',

            },
             showarrow: false,
            };
            layout.annotations.push(annotation);

    }
    Plotly.newPlot('grid_2', data, layout);
}

function update_colored_bars(error, graph_data, colors) {

    let y = Object.keys(graph_data["current_value"]).reverse();

    // Ordernar lista de colores:
    let clr_ls =[];
    let left_margin = 3;

    if (Array.isArray(colors)) {
            clr_ls = colors.reverse();
    }

    for(let ix in y){

        if (!Array.isArray(colors)) {
            clr_ls.push(colors[y[ix]]);
         }

        y[ix] = y[ix].replace("Posición", "P. ")

        if( y[ix].length > 20){
            y[ix] = y[ix].slice(0, 20);
        }
        y[ix] = y[ix].toUpperCase();
        left_margin = Math.max(left_margin, y[ix].length)
    }
    // transformar en mayúsculas:
    // y = y.map(function (value, idx) { return value.toUpperCase(); });
    let x = Object.values(graph_data["current_value"]).reverse();

    let x_d = Object.values(graph_data["dif"]).reverse();
    let x_p = Object.values(graph_data["percentage"]).reverse();
    let text_p = [], text_d =[];
    for(let ix in x_d){
        a_t = "max: " +  format_w_spaces(x_d[ix] + x[ix]) + "MW";
        text_p.push(a_t);
        text_d.push(x[ix] + " MW");
    }

    let data = [
        {
            x: x, y: y, type: 'bar', orientation: 'h',
            //text: text_d,
            textposition: 'auto', name: "Region",
            hoverinfo: 'none',
            marker: {
                color: clr_ls,
                opacity: 1
            }
        },
        {
            x: x_d, y: y, type: 'bar',
            orientation: 'h',
            text: text_p,
            // textposition: 'auto',
            align:'right',
            hoverinfo: 'text',
            marker: {
                color: 'rgba(64, 64, 64, 0.8)',
                opacity: 0.8
            }
        }
    ];

    let layout = get_layout_bar();
    left_margin = left_margin*8.5;
    layout.margin = {
            l: left_margin,
            r: 35,
            b: 20,
            t: 20,
            pad: 0
        };

     if(y.length <= 3){
        layout.margin.t = 100;
        layout.margin.b = 100;
     }

     if(y.length <= 1){
        layout.margin.t = 150;
        layout.margin.b = 150;
     }

    let dist = Math.max.apply(null, x) + 1.5*Math.max.apply(null, x_d) ;
    for(let i = 0 ; i < y.length ; i++){
        let annotation = {
            xref: 'x1',
            yref: 'y1',
            x: dist,
            y: y[i],
            text: '<b>'+ x_p[i] + '</b>',
            align: 'left',
            font: {
              //family: 'Arial',
              size: 12,
              color: 'white',

            },
             showarrow: false,
            };
            layout.annotations.push(annotation);

            /*if(x[i] < 0.15*dist){
                ds_x = 0.15*dist;
            }else{
                ds_x = x[i];
            }*/

            annotation = {
            xref: 'x1',
            yref: 'y1',
            x: dist*0.05,
            y: y[i],
            text: '<b>'+ format_w_spaces(x[i]) + '</b>',
            align: 'left',
            font: {
              //family: 'Arial',
              size: 12,
              color: 'rgb(255, 255, 255)',

            },
             showarrow: false,
            };
            layout.annotations.push(annotation);

    }
    Plotly.newPlot('grid_2', data, layout);

    function fill(N, func) {
        var empty = Array.apply(null, Array(N));
        return empty.map(func);
    }

    return true;
}

function default_background(){
    return 'black';
}

function get_default_layout(){
    return {
                showlegend: false,
        margin: {
                l: 80,
                r: 45,
                b: 40,
                t: 35,
                pad: 0
                },
        font:{size:12, color:'#ffffff'},
        paper_bgcolor: default_background(),
        //paper_bgcolor: 'rgba(37,97,142,1)',
        //plot_bgcolor: 'rgba(37,97,142,1)',
        plot_bgcolor: default_background(),
        xaxis:{
            tickcolor:"white",
            gridcolor:'gray',
            linecolor:'gray',
            showline:true,
            showgrid:false,
        },
        yaxis: {
            tickcolor:"white",
            gridcolor:'gray',
            linecolor:'gray',
            // range:general_range,
            autorange: true,
            showline:true,
            showgrid:false,
        },
        annotations: [{
            xref: 'paper',
            yref: 'paper',
            x: -0.095,
            xanchor: 'right',
            y: 0.5,
            yanchor: 'center',
            text: 'DEMANDA NACIONAL   [MW]',
            showarrow: false,
            textangle: 270,
            font: {
                size: 14
             }
        }]

    };
}

function get_layout_bar( ){

    return {
        showlegend: false,
        barmode: 'stack',
        annotations: [],
        margin: {
            l: 170,
            r: 10,
            b: 20,
            t: 20,
            pad: 0
        },
        font: {size: 11, color: '#ffffff', family: "Tahoma, Charcoal, sans-serif"},
        paper_bgcolor: default_background(),
        //paper_bgcolor: 'rgba(37,97,142,1)',
        plot_bgcolor: default_background(),
        xaxis:{

            gridcolor:'gray',
            linecolor:'gray',
            showticklabels:false,
            showgrid:false,
            zeroline:false,
            showline:false,
        },
        yaxis: {
            //tickcolor:"white",
            gridcolor:'gray',
            linecolor:'gray',
            showgrid:false,

        }
    };


}


function update_stacked_trend(error, graph_data, color_ls, title) {
    let layout = get_default_layout();
    let n_traces = [];
    let x, acc, last_value, ix=0;
    let color_fill = {}

    for(let id in graph_data){
        g_data = graph_data[id];
        let y =  Object.values(g_data);
        let text = [];

        if (Array.isArray(color_ls)) {
            color_fill[id] = color_ls[ix++];
        }else{
            color_fill = color_ls;
        }

        // acumulando para realizar stacked area plot
        if(acc === undefined){acc = y;}
        else{
            let sum = acc.map(function (num, idx) {
                if(y[idx] != null){return num + y[idx];}
                else{return null;}
            });
            acc = sum;
        }
        // creando las etiquetas:
        for(let i in y){
            let t_i = "(" + format_w_spaces(acc[i])  + " MW ; " + format_w_spaces(y[i]) + " MW)";
            if(y[i] != null){
                last_value = acc[i];
            }
            text.push(t_i);
        }
        let trace = {
            x: Object.keys(g_data),
            y: Object.values(g_data),
            type: 'scatter',
            name: id.toUpperCase(),
            textposition: 'top',
            text: text,
            mode: 'lines',
            hoverinfo: 'text+name',
            fill: 'tonexty',
            fillcolor: color_fill[id],
            line: {
                color: color_fill[id],
                width: 1
            }
        }
        n_traces.push(trace);
    }
    traces = stackedArea(n_traces);
    layout.annotations[0].text = title.toUpperCase();

    Plotly.react('grid_1', traces, layout);


    if( title === "DEMANDA NACIONAL [MW]"){

    d3.select('#demanda')
        .text(  format_w_spaces(parseInt(last_value)));

        d3.select('#id_note')
            .text("2.");

        d3.select('#info')
            .text("2. Demanda en puntos de entrega");
    }
    return true;
}



function update_trend(error, graph_data, labels, ls_color) {
    let layout = get_default_layout();

    let g_current = graph_data[1]["Demanda nacional"];

    let x = Object.keys(g_current);
    let traces = [];
    let y;

    for(let id in graph_data){

        let g_data = graph_data[id]["Demanda nacional"];
        let y_value = Object.values(g_data);
        y = y_value;
        // load_trend(x, y, layout, 'grid_1');
        let color_line;
       if(id === "0"){
            color_line = 'rgba(255,255,255,0.4)';
        }else{
            color_line = ls_color[id];
        }
        let trace1 = {
            x: x,
            y: y_value,
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            name: labels[id],
            fillcolor : ls_color[id],
            line: {
                // color: 'rgba(255,255,255,1)',
                color: color_line,
                width: 2,
                simplify:false
            }
        };
        traces.push(trace1)



    }

    layout.yaxis.range = general_range;
    layout.yaxis.autorange = false;
    // Plotly.plot('grid_1', [trace1], layout);
    Plotly.react('grid_1', traces, layout);
    /* actualizar valor de demanda nacional*/
    let last_value = 0;
    for(let i=0;i < y.length; i++){
        if(y[i] != null){
            last_value = y[i];
        }else{
            break;
        }
    }

    d3.select('#demanda')
        .text( format_w_spaces( Math.round(last_value)));

    d3.select('#id_note')
        .text("1.");

    d3.select('#info')
        .text("1. Demanda en bornes de generación");


}


function plot_sankey(error, sankey_data, title) {

    let units = "MW";

    let size_grid = get_height_width("#grid_3");
    margin = {top: 20, right: 10, bottom: 15, left: 10},
        width = size_grid["width"] - margin.left - margin.right,
        height = size_grid["height"] - margin.top - margin.bottom;


    d3.select("#grid_3").selectAll("*").remove();

    // append the svg canvas to the page
    let svg_container = d3.select("#grid_3")
        .style("background", default_background())
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // Set the sankey diagram properties
    let sankey = d3.sankey()
        .nodeWidth(30)
        .nodePadding(10)
        .size([width, height]);

    // set the color scale for the sankey:

    let colors =  [];
    let conf_color = {
        "Producción": "#ccccb3",
        "Importación": "#cc0000",
        "Exportación": "#0e283b",
        "Demanda Nacional": "#ffaa00",
        "Hidroeléctrica":"#80bfff",
        "Termoeléctrica":"#AC8749",
        "No convencional":"#009900",
        "Costa"       :"rgba(100, 10, 10, 1)",
        "Sierra"      :"#0e283b",
        "Oriente"     :"rgba(0, 74, 86, 1)",
        "Pérdidas"    :"rgba(255, 10, 10, 1)",
        "CNEL"        :"#64467d",
        "Empresas Eléctricas"    :"#4e93c5",
        "S.N.I"       :"#a05e83",
        "Gen. Inmersa"     :"#aeb316",
        "Gen. Local"       :"#5b5b5b"
    };

    // set generacion total, exportación, importación
    let res = {produccion_mw : 0, importacion_mw: 0, exportacion_mw : 0};
    let nodes = [];
    for(let id in sankey_data){
        let d = sankey_data[id];
        if(d.target === "Producción"){  res.produccion_mw += d.value;}
        if(d.source === "Importación"){ res.importacion_mw = d.value;}
        if(d.target === "Exportación"){ res.exportacion_mw = d.value;}
        if(!is_in(d.target,nodes)){
            nodes.push(d.target);
        }
        if(!is_in(d.source, nodes)){
            nodes.push(d.source);
        }
    }

    if(title === "Demanda Nacional"){
        for(let id in res){
            d3.select("#" + id)
                .text( format_w_spaces(res[id]) );
        }
    }

    nodes.forEach(function (d) {

         if( conf_color[d] === undefined){
             if( d.search("Demanda") >= 0) { colors.push("#ffaa00");}
             else{
                 colors.push("#a7a3a8");
             }
         }
         else{
            colors.push(conf_color[d]);
         }

    });

    let color_scale = d3.scale.ordinal()
        .domain(nodes)
        .range(colors);




    dw_sankey = draw_sankey(sankey, svg_container, sankey_data, units, color_scale);
    return dw_sankey;
}




/*
function update_pie_demanda(error, graph_data) {

    let y = Object.keys(graph_data["current_value"]);
    let x = Object.values(graph_data["current_value"]);
    let data = [{
        values: x,
        labels: y,
        type: 'pie',
        textposition: 'inside'
    }];

    let layout = {
         margin: {
            l: 20,
            r: 10,
            b: 10,
            t: 20,
            pad: 0
        },
        paper_bgcolor: 'rgba(37,97,142,1)',
        plot_bgcolor:
    };

    Plotly.newPlot('grid_3', data, layout);'rgba(37, 97, 142,0.2)'

}*/


/*
function load_trend(x, y, layout, to_plot) {
    let n = x.length;
    let y_p = createArray(n, null);
    let trace1 = {
        x: x,
        y: y_p,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        fillcolor : 'rgba(250, 250, 250, 0.5)',
        line: {
            color: 'rgb(26, 0, 0)',
            width: 2,
            simplify:false
        }
    };
    Plotly.plot(to_plot, [trace1], layout);

    let step = 20;
    for(i = step; i <= x.length; i=i+step){
        let n_i = parseInt(i);
        y_p = y.slice(0, n_i);
        y_p = y_p.concat(createArray(n-n_i,null));
        Plotly.animate(to_plot, {
                data: [{y: y_p, x:x}],
                layout: layout,
              }, {
                transition: {
                  duration: 1,
                  //easing: 'cubic-in-out'
                  easing: 'elastic-in'
                }
              })
    }
}
*/