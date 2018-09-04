function nivel_global(){
    draw_ecuador_in_world('main_grid');
    barras_demanda();
    tendencia_demanda_nacional();
    sankey_nacional();
}

function nivel_regional() {
    draw_ecuador_only('main_grid');
    pintar_regiones_del_ecuador();
    mover_regiones();

}




//------------------------------------------------------------------------------------------------------
//  FUNCIONES AUXILIARES:

function sankey_nacional() {

    url = '/cal/informacion_sankey_generacion_demanda';
    queue()
        .defer(d3.json, url)
        .await(plot_sankey);
}


function tendencia_demanda_nacional(){

    let url = '/cal/demanda_nacional_desde_sivo';
    queue()
        .defer(d3.json, url)
        .await(update_trend);

    url = '/cal/maxima_demanda_nacional';
    queue()
        .defer(d3.json, url)
        .await(plot_maxima_demanda);
}

function barras_demanda(){
    let last_time = time_last_30_min();
    let url = '/cal/demanda_empresas/'+ last_time.toISOString() + "&7";
    queue()
        .defer(d3.json, url)
        .await(update_barras_demanda);
}


function plot_maxima_demanda(error, graph_data) {

    let data = graph_data[0];
    let generacion_maxima = data["MW_Generacion"];
    let demanda_maxima = data["MW_Demanda"];
    let layout = {
        shapes: [
        {
            type: 'line',
            xref: 'paper',
            x0: 0,
            y0: demanda_maxima,
            x1: 1,
            y1: demanda_maxima,
            line:{
                color: '#ffaa00',
                width: 2,
                dash:'dot'
            }
        }],
        annotations: [{
            xref: 'paper',
            yref: 'paper',
            x: -0.08,
            xanchor: 'right',
            y: 0.5,
            yanchor: 'center',
            text: 'DEMANDA NACIONAL',
            showarrow: false,
            textangle: 270
        }]
    };

    let today = new Date();
    today = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + " " + data["Hora"];

    let trace1 = {
          x: [today],
          y: [demanda_maxima],
          mode: 'lines+markers+text',
          name: data["Fecha"],
          text: ['máxima demanda histórica'],
          textposition: 'top',
          type: 'scatter'
    };
    Plotly.relayout('grid_1', layout);
    Plotly.addTraces('grid_1', [trace1]);
}



function update_barras_demanda(error, graph_data) {

    let y = Object.keys(graph_data["current_value"]).reverse();
    let x = Object.values(graph_data["current_value"]).reverse();

    let x_d = Object.values(graph_data["dif"]).reverse();
    let x_p = Object.values(graph_data["percentage"]).reverse();

    let data = [
        {
            x: x, y: y, type: 'bar', orientation: 'h',
            text: x,
            textposition: 'auto', name: "Empresa",
            hoverinfo: 'none',
            marker: {
                color: 'rgba(14, 40, 59, 0.8)',
                opacity: 1
            }
        },
        {
            x: x_d, y: y, type: 'bar',
            orientation: 'h',
            // text: x_p,
            // textposition: 'auto',
            align:'right',
            hoverinfo: 'none',
            marker: {
                color: 'rgba(217, 217, 217, 0.8)',
                opacity: 0.5
            }
        }
    ];
    let layout = {
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
        font: {size: 9, color: '#ffffff'},
        paper_bgcolor: 'rgba(37,97,142,1)',
        plot_bgcolor: 'rgba(37, 97, 142,0.2)',
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
    let dist = Math.max.apply(null, x) + Math.max.apply(null, x_d) + 100;
    for(let i = 0 ; i < y.length ; i++){
        let annotation = {
        xref: 'x1',
        yref: 'y1',
        x: dist,
        y: y[i],
        text: '<b>'+ x_p[i] + '</b>',
        font: {
          //family: 'Arial',
          size: 11,
          color: 'rgb(15, 15, 15)',

        },
         showarrow: false,
        };
        layout.annotations.push(annotation);
    }
    Plotly.newPlot('grid_2', data, layout);
}


function update_trend(error, graph_data) {
    let layout = {
                showlegend: false,
                legend: {
                    orientation: "h",
                    font: {size: 9},
                    x: 0.1,
                    y: 1.35,
                    xanchor: "center",
                    xref:'container',
                    //traceorder:'normal',

                },
        margin: {
                l: 60,
                r: 40,
                b: 40,
                t: 25,
                pad: 0
                },
                barmode:'stack',
        font:{size:9, color:'#ffffff'},
        paper_bgcolor: 'rgba(37,97,142,1)',
        // paper_bgcolor: 'rgba(71,34,34,1)',
        // plot_bgcolor: 'rgba(37, 97, 142,0.2)',
        plot_bgcolor: 'rgba(37,97,142,1)',
        //plot_bgcolor: 'rgba(37,97,142,1)',
        // title: "DEMANDA NACIONAL",
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
            range:[1800, 4000],
            autorange: false,
            showline:true,
            showgrid:false,
        },

    };


    let g_data = graph_data["Demanda nacional"];

    let x = Object.keys(g_data);
    let y = Object.values(g_data);
    // load_trend(x, y, layout, 'grid_1');
    let trace1 = {
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        name: 'Demanda',
        fillcolor : 'rgba(255, 255, 255, 0.5)',
        line: {
            color: 'rgba(14, 40, 59, 0.8)',
            width: 3,
            simplify:false
        }
    };
    Plotly.react('grid_1', [trace1], layout);

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
        .text(parseInt(last_value));
}


function plot_sankey(error, sankey_data) {

    let units = "MW";

    let size_grid = get_height_width("#grid_3");
    margin = {top: 10, right: 10, bottom: 15, left: 10},
        width = size_grid["width"] - margin.left - margin.right,
        height = size_grid["height"] - margin.top - margin.bottom;



    // append the svg canvas to the page
    let svg_container = d3.select("#grid_3")
        .style("background", "rgba(37,97,142,1)")
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

    let color_scale = d3.scale.ordinal()
                       .domain([ ])
                               .range([ "#80bfff", //"#0e283b",
                                   "#ccccb3",
                                   "#AC8749",
                                   "#009900",
                                   "#ffaa00",
                                   "#e60000",
                                   "#0e283b"]);


    // set generacion total, exportación, importación
    let res = {produccion_mw : 0, importacion_mw: 0, exportacion_mw : 0};
    for(let id in sankey_data){
        let d = sankey_data[id];
        if(d.target === "Producción"){
            res.produccion_mw += d.value;
        }
        if(d.source === "Importación"){
            res.importacion_mw = d.value;
        }
        if(d.target === "Exportación"){
            res.exportacion_mw = d.value;
        }
    }

    for(let id in res){
        d3.select("#" + id)
            .text( format_w_spaces(res[id]) );
    }


    draw_sankey(sankey, svg_container, sankey_data, units, color_scale);

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
        plot_bgcolor: 'rgba(37, 97, 142,0.2)'
    };

    Plotly.newPlot('grid_3', data, layout);

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