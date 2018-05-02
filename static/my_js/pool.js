/**
 * Created by Roberto on 5/1/2018.
 * Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
 * Mateo 6:33
 */
let class_;

function update_values_for(class_to_refresh){
    class_ = class_to_refresh;
    let tags_div = d3.selectAll("." + class_);
    let tags = tags_div[0];
    console.log(tags);
    for(let t in tags){
        if(t === 'parentNode'){continue;}
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

    d3.select('[id="'+id+'"]').text(value);
}