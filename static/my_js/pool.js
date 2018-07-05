/**
 * Created by Roberto on 5/1/2018.
 * Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
 * Mateo 6:33
 */
let class_;

function update_values_for(class_to_refresh){
    class_ = class_to_refresh;
    let tags_div = d3.selectAll("." + class_);
    //let tags = tags_div["_groups"][0]; // d3_v4 !!
    let tags = get_groups(tags_div);
    // console.log(tags);
    for(let t in tags){
        if( !Number.isInteger(parseInt(t))){continue;}
        // console.log(t);
        let id = tags[t].id;
            let url = '/tag/' + id;
            queue()
                .defer(d3.json, url)
                .await(update_value)
    }
}

function update_value(error, json_data) {
    let id = json_data.id;
    let value = json_data.value;
    try{
        value = numberWithSpaces(value);
    }catch (e) {
        
    }
    // console.log(current_timestamp);
    d3.select('[id="'+id+'"]').text(value);

    current_timestamp = get_time();
}

function get_time() {
    let ct = new Date();
    let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return (ct.toLocaleDateString("es-US",options) + ", " + ct.toLocaleTimeString());
}

function capitalizeFirstLetter(string) {
    try{
        return string.charAt(0).toUpperCase() + string.slice(1);
    }catch (e) {
        return string;
    }
}

function update_time(id) {
    current_timestamp = get_time();
    d3.select('[id="'+ id +'"]').text(
        capitalizeFirstLetter(current_timestamp)
    );
}

const numberWithSpaces = (x) => {
  let parts = x.toString().split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  return parts.join(".");
};