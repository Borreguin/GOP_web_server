main(selected_level);

function main(detail){

    if(detail === "global"){
        history.pushState('global', 'Detalle global', '/map');
        nivel_global();
        // window.location.replace("/map");
    }
    else if(detail === "regional"){
        history.pushState('global', 'Detalle global', '/map/regional');
        nivel_regional();
        // window.location.replace("/map/regional");
    }
    else if(detail === "empresarial"){
        history.pushState('global', 'Detalle global', '/map/empresarial');
        nivel_empresarial();
        // window.location.replace("/map/empresarial");
    }
    else if(detail === "provincial"){
        history.pushState('global', 'Detalle global', '/map/provincial');
        nivel_provincial();
        // window.location.replace("/map/empresarial");
    }

}

function seleccionar_mapa(title){
     if(title === "Ecuador"){
            history.pushState('global', 'Detalle global', '/map/regional');
            nivel_regional();
            //window.location.replace("/map/regional");
     }
     if(is_in(title, ecuador_regions)){
        /*modal.style.display = "block";
        d3.select('#modal_title')
            .text(title);*/

        last_time = time_last_30_min();
        let stamp_time = to_yyyy_mm_dd_hh_mm_ss(last_time)

        queue()
              // .defer(draw_ecuador_only, 'main_grid')
              .defer(d3.json, '/cal/tendencia_demanda_por_provincia/' + title )
              .defer(d3.json, '/cal/informacion_sankey_generacion_demanda_nivel_empresarial/' + stamp_time)
              .defer(d3.json, '/cal/demanda_por_provincia/' + title)
              .await(function(error, js_dm_emp, js_sankey, js_barras){
                    if(error) throw error;
                    // ec_map = pintar_por_empresas(ec_map);
                    dw_sankey = plot_sankey(error, js_sankey);
                    n_c = Object.keys(js_dm_emp).length;
                    let colors = color_band.slice(0,n_c);
                    st1 = update_stacked_trend(error, js_dm_emp, colors, title + " [MW]");
                    st2 = update_colored_bars(error, js_barras, colors);
                    if(dw_sankey != undefined && st1 != undefined && st2 != undefined){
                        mover_regiones();
                        stop_all();
                    }

               });

     }
}