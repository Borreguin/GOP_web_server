$('#datepicker').datepicker({
    todayBtn: "linked",
    language: "es",
    format: "yyyy-mm-dd",
    todayHighlight: true
});
let gridcolor = '#a39ba4';
let time_minutes = 12;
let styles = {white_style: "white", black_style: "black"};
let font_color = {"black_style": "white", "white_style": "black"};
let js_data_global;
let current_style = "black_style";
let range_y2 = [];
let loading = false;

now = new Date();
tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
d3.select("#ini_date").property("value", to_yyyy_mm_dd(now));
d3.select("#end_date").property("value", to_yyyy_mm_dd(tomorrow));

actualizar();


function actualizar() {
    ini_date = d3.select("#ini_date").property("value");
    end_date = d3.select("#end_date").property("value");
    if(loading===false){
        graficar_tendencia(ini_date, end_date);
        setTimeout(actualizar, time_minutes*1000*60);
    }
}

function graficar_tendencia(ini_date, end_date){
    d3.select("#info")
        .text("Espere por favor, la gráfica puede tomar varios minutos dependiendo del periodo de consulta");
    loading = true;
    queue()
      // .defer(draw_ecuador_only, 'main_grid')
      .defer(d3.json, '/cal/tendencia_reserva_de_generacion/' + ini_date + "&" + end_date)
      .await(function(error, js_data){
            if(error) throw error;
            loading = false;
            d3.select("#info").text("");
            let labels = ["timestamp", "p_disponible_linea", "p_efectiva", "p_disponible_total",
                "p_indisponible_total", "p_efectiva_linea", "p_generacion", "p_indisponible_linea",
                    "p_reserva"];
            js_data = transpose_data(js_data, labels);
            plot_data(js_data);
       });

}

function plot_data(js_data){

    let to_plot_1 = [ "p_efectiva", "p_disponible_total", "p_generacion", "p_disponible_linea", "p_reserva"];

    let names = {"p_disponible_linea": "Disponible rodante",
        "p_efectiva": "Efectiva instalada total",
        "p_disponible_total": "Disponible Total",
        "p_generacion": "Producción Nacional",
        "p_reserva" : "Reserva"
    };

    let fill = {"p_disponible_linea": 'tonexty',
        "p_efectiva": null,
        "p_disponible_total": null,
        "p_generacion": null,
        "p_reserva" : null

    };
    let color = {
        "p_disponible_linea": '#4eb37b',
        "p_efectiva": '#2d7dff',
        "p_disponible_total": '#b32f1c',
        "p_generacion": '#ffb224',
        "p_reserva" : '#4eb37b'

    };

    let yaxis = {"p_disponible_linea": "y", "p_efectiva": "y", "p_disponible_total": "y",
        "p_generacion": "y", "p_reserva": "y2"};
    let mode = {"p_disponible_linea": "lines", "p_efectiva": "lines", "p_disponible_total": "lines",
        "p_generacion": "lines", "p_reserva": "lines+markers+text"};

    graph_data = [];
    for(let ix in to_plot_1){
            let idx = to_plot_1[ix];
            let trace = {
                x: js_data["timestamp"],
                y: js_data[idx],
                name: names[idx],
                fill: fill[idx],
                yaxis: yaxis[idx],
                type: 'scatter',
                mode: mode[idx],
                line: {color: color[idx]}

            };
            if(idx === "p_reserva"){
                n = parseInt(js_data[idx].length / 10);
                d = js_data[idx];
                t = js_data["timestamp"];
                text = [];
                let min_v = 1000, max_v = 0;
                for(let i in d){
                    let str_t =  t[i];
                    if(d[i]<min_v){ min_v = d[i];}
                    if(d[i]>max_v){ max_v = d[i];}

                    if(i % n === 0 && n <= 5){
                        text.push(parseInt(d[i]));
                    }
                    else if(str_t.search("19:30") > 0){
                        text.push(parseInt(d[i]));
                    }
                    else{
                        text.push(null);
                    }
                }
                trace.text = text;
                trace.textposition= 'bottom';
                trace.textfont ={
                        'family': 'Verdana',
                        'size' : 18,
                        'color' : font_color[current_style]
                    };
                range_y2 = [min_v*0.2, max_v*1.3];
            }
            graph_data.push(trace);
    }
    let layout = get_layout(current_style);
    layout.yaxis2.range = range_y2;

    js_data_global = js_data;
    Plotly.newPlot("grid_1", graph_data, layout);
    add_sytles();
}



function get_layout(style) {

    paper_bgcolor = {"black_style": "#0f0f0f",
        "white_style": "#eaeaea"};
    plot_bgcolor = {"black_style": "black",
        "white_style": "#ffffff"};

    let layout = {
        yaxis: {
            domain: [0, 0.7],
            gridcolor: gridcolor,
            tickcolor: font_color[style]
        },
        yaxis2: {
            domain: [0.8, 1],
            gridcolor: gridcolor,
            tickcolor: font_color[style]
        },
        xaxis: {
            gridcolor: gridcolor,
            tickcolor: font_color[style]
            // dtick: 1000 * 60 * 60,
            // tickformat: '%H',
        },
        font: {}

    };
    layout.legend = {"orientation": "h", x: -0.05, y: 1.1};
    layout.paper_bgcolor = paper_bgcolor[style];
    layout.plot_bgcolor = plot_bgcolor[style];
    layout.font.color = font_color[style];
    return layout;
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
            .html('<a rel="tooltip" class="modebar-btn" data-title="Seleccione el estilo deseado" > sty' +
                   '</a>')
            .on("click", function() {
                style = d3.select(this).attr("id");
                current_style = style;
                plot_data(js_data_global);
            });
    }
}