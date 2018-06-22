/**
 * Created by Roberto on 5/1/2018.
 * Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
 * Mateo 6:33
 */

// _____________________________________________________________________________________________________
// General variables to be used in any script:
// !! Don´t change this general values !!
let margin = {
        top: 5,
        right: 5,
        bottom: 5,
        left: 5
};

let ct = new Date();
let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
let current_timestamp = ct.toLocaleDateString("es-US",options) + ", " + ct.toLocaleTimeString();
let bar_size = 160;
let w = $(document).width();
let h = $(document).height();
let height =  Math.max(Math.min(h, 800), 300) - margin.top - margin.bottom - bar_size;
let width = Math.max(Math.min(w, 1200), 500) - margin.left - margin.right;

// End general declaration
//_______________________________________________________________________________________________________

// Gets the height and width:
function get_height_width(to_plot) {
    let borders = d3.select(to_plot).node().getBoundingClientRect();
    if(borders.width > 100) { width = borders.width - margin.right - margin.left;}
    if(borders.height > 100) { height = borders.height - margin.bottom - margin.top;}
    return {
        width: width,
        height: height
    };
}

// return a scale of colors:
function color_scale(color_list) {
    let res_color_scale;
    try{
        // d3.v4:
        res_color_scale = d3.scaleOrdinal().range(color_list);
    }catch (e)
    {   // d3.v3:
        res_color_scale = d3.scale.ordinal().range(color_list);
    }
    return res_color_scale;
}
// solve problems of compatibility between d3 v4 and d3 v3
function scaleLinear(objt){
    let scale_res;
    try {
        scale_res = d3.scaleLinear().domain(objt.domain).range(objt.range);
    }catch (e) {
        scale_res = d3.scale.linear().domain(objt.domain).range(objt.range);
    }
    return scale_res;
}

function get_groups(objt) {
    let grps;
    try{
        grps = objt["_groups"][0]; // d3_v4 !!
    }
    catch (e) {
        grps = objt[0];  // d3_v3
    }
    return grps;
}