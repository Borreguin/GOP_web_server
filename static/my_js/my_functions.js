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
//let w = $(document).width();
let w = document.documentElement["clientWidth"];
let h = document.documentElement["clientHeight"];
let height =  Math.max(Math.min(h, 950), 300) - margin.top - margin.bottom - bar_size;
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

function add_time(ct_date, int_time_minutes){
    return new Date(ct_date.getTime() + int_time_minutes*60000);
}

function createArray(len, itm) {
    if(len > 0){
        let arr1 = [itm],
            arr2 = [];
        while (len > 0) {
            if (len && 1) arr2 = arr2.concat(arr1);
            arr1 = arr1.concat(arr1);
            len >>>= 1;
        }
        return arr2;
    }
    else{
        return [];
    }
}

function time_last_15_min(){
    let dCurrent = new Date();
    let m = dCurrent.getMinutes();
    if( 0< m && m <15){
        dCurrent.setMinutes(0);
    }else if(15 < m && m  <30){
        dCurrent.setMinutes(15);
    }else if(30< m && m  < 45){
        dCurrent.setMinutes(30);
    }else if(45< m && m  <60){
        dCurrent.setMinutes(45)
    }
    dCurrent.setSeconds(0);
    dCurrent.setMilliseconds(0);
    return dCurrent;
}

function time_last_30_min(){
    let dCurrent = new Date();
    let m = dCurrent.getMinutes();
    if( 0< m && m <30){
        dCurrent.setMinutes(0);
    }else if(m > 30){
        dCurrent.setMinutes(30)
    }
    dCurrent.setSeconds(0);
    dCurrent.setMilliseconds(0);
    return dCurrent;
}


let formatNumber = d3.format(",.0f"),    // zero decimal places
format_w_spaces = function (d) {
    return formatNumber(d).replace(/,/g, ' ').replace(/\./, ',');
};

function time_now() {
    dt = new Date();
    return to_yyyy_mm_dd_hh_mm_ss(dt);
}

function stop_all(){
    try {
        window.stop();
    } catch (exception) {
        document.execCommand('Stop');
    }
}

function stackedArea(traces) {
	for(var i=1; i<traces.length; i++) {
		for(var j=0; j<(Math.min(traces[i]['y'].length, traces[i-1]['y'].length)); j++) {
		    if(traces[i-1]['y'][j] != null){
			    traces[i]['y'][j] += traces[i-1]['y'][j];
			}else
			{
			    traces[i]['y'][j] = null;
			}

		}
	}
	return traces;
}

function transpose_data(js_data, labels){

    let ds = {};
    for(let ix in labels){ds[labels[ix]] = [];}
    if(js_data[0] !== undefined) {
        js_data.forEach(function (e) {
            for (let ix in labels) {
                ds[labels[ix]].push(e[labels[ix]]);
            }
        });
    }
    return ds;
}

function to_yyyy_mm_dd_hh_mm_ss(ct){

    return ct.getFullYear() + "-" + (ct.getMonth()+1) + "-" + ct.getDate() + " "
            + ct.getHours() + ":" + ct.getMinutes() + ":" + ct.getSeconds();
}

function to_yyyy_mm_dd(ct){

    return ct.getFullYear() + "-" + ("0" + (ct.getMonth() + 1)).slice(-2) + "-" + ("0" + ct.getDate()).slice(-2);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function transponer(js_object){

    let js_keys = Object.keys(js_object);
    let indexs = Object.keys(js_object[js_keys[0]]);
    let t_data = [];

    for(let idx in indexs){
        let register = {};
        register["ID"] = Object.keys(js_object[js_keys[0]])[idx];
        for(let i in js_keys){
            register[js_keys[i]] = js_object[js_keys[i]][indexs[idx]];
        }
        t_data.push(register)
    }

    return t_data;
}

/*
queue()
    .defer(f1, "Vamos")
    .defer(f2, "tiene que salir")
    .await(f3);

function f1(str1, callback){
    console.log("f1:" + str1);
    error = null;
    callback(error, str1);
}

function f2(p2, callback){
    console.log("f2:" + p2);
    error = null;
    callback(error, p2);
}

function f3(error, str1, str2){
    console.log("f3:" + str1 + str2);
    return str1 + str2;
}*/