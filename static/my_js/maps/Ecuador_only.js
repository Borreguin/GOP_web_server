let map;
let otro_pais_color = "rgba(51, 77, 77,1)";


function draw_ecuador_only(to_plot, callback){
	
	map = AmCharts.makeChart( to_plot, {
					"type": "map",
					//"pathToImages": "http://www.amcharts.com/lib/3/images/",
					"creditsPosition": "bottom-right",
					"addClassNames": true,
					"fontSize": 15,
					"color": "#FFFFFF",
					"projection": "mercator",
					"backgroundAlpha": 1,
					//"backgroundColor": "rgba(37,97,142,1)",
					"backgroundColor": "black",

					"dataProvider": {
						"map": "ecuadorLow",
						"getAreasFromMap": true,
						"images": [
                            /*{   "label": "(1, -88)",
                                "latitude": 1.4,
                                "longitude": -83.55,
                                "labelColor": "rgba(180,180,180,1)"
                            },
                            {   "label": "(1, -92)",
                                "latitude": 1.4,
                                "longitude": -86.5,
                                "labelColor": "rgba(180,180,180,1)"
                            },
                            {   "label": "(2, -92)",
                                "latitude": -1.22   ,
                                "longitude": -86.5,
                                "labelColor": "rgba(180,180,180,1)"
                            }*/
                        ],
						"zoomLatitude": -1.75,
						"zoomLongitude": -83.5,
						"zoomLevel": 2.2,
						"areas": [
							{ "id": "PE-AMA", "color": otro_pais_color},
							{ "id": "PE-LOR", "color": otro_pais_color},
							{ "id": "PE-TUM", "color": otro_pais_color},
							{ "id": "PE-PIU", "color": otro_pais_color},
							{ "id": "PE-CAJ", "color": otro_pais_color},
							{ "id": "PE-SAM", "color": otro_pais_color},
							{ "id": "PE-LAM", "color": otro_pais_color},
							{ "id": "CO-NAR", "color": otro_pais_color},
							{ "id": "CO-AMA", "color": otro_pais_color},
							{ "id": "CO-PUT", "color": otro_pais_color},
							{ "id": "CO-CAQ", "color": otro_pais_color},
							{ "id": "CO-CAU", "color": otro_pais_color},
							{ "id": "CO-HUI", "color": otro_pais_color}
						],

                        "lines": [{
                            "latitudes": [ 1.5 ,1.5, -0.7, -1.3, -1.3, 1.5],
                            "longitudes": [ -85.2 ,-82, -82, -82.5, -85.2, -85.2]
                        }],
					},

					"balloon": {
						"horizontalPadding": 15,
						"borderAlpha": 0,
						"borderThickness": 2,
						"verticalPadding": 15
					},
					"areasSettings": {
						"color": "#0e283b",
						"outlineColor": "rgba(37,97,142,1)",
						"rollOverOutlineColor": "rgba(255,0,142,1)",
						"rollOverColor": "rgba(255, 170, 0, 0.8)",
						"rollOverBrightness": 20,
						"selectedColor": "rgba(255, 170, 0, 0.8)",
						"selectedBrightness": 0,
						"selectable": true,
						"unlistedAreasAlpha": 0,
						"unlistedAreasOutlineAlpha": 0,
							"autoZoom": false,
							"outlineThickness": 1.5
					},
					"imagesSettings": {
						"alpha": 1,
						"color": "rgba(35,29,29,1)",
						"outlineAlpha": 0,
						"rollOverOutlineAlpha": 0,
						"outlineColor": "rgba(37,97,142,1)",
						"rollOverColor": "rgba(37,97,142,1)",
						"rollOverBrightness": 20,
						"selectedBrightness": 1,
						"selectable": true
					},
					"linesSettings": {
						"color": "rgba(180,180,180,1)",
						"selectable": true,
						"rollOverBrightness": 20,
						"selectedBrightness": 20
					},
					"listeners": [ {
		    				"event": "clickMapObject",
						    "method": function( event ) {
						     // deselect the area by assigning all of the dataProvider as selected object
						     map.selectedObject = map.dataProvider;
							 let selected_region = event.mapObject.title;
							 // console.log(event.mapObject);

						if(is_in(selected_region, ecuador_regions)){
                            // toggle showAsSelected
                            event.mapObject.showAsSelected = !event.mapObject.showAsSelected;

                            // bring it to an appropriate color
                            map.returnInitialColor( event.mapObject );

                            // let's build a list of currently selected states
                            for ( let i in map.dataProvider.areas ) {
                                    let area = map.dataProvider.areas[ i ];
                                    if ( area.title === selected_region && is_in(area.title, ecuador_regions) ) {

                                        area.colorReal =  "rgba(255, 150, 0, 1)";
                                    }
                                    else{
                                        area.colorReal =  "#0e283b";
                                    }
                                }
                            // set same zoom levels to retain map position/zoom in case a selection was made after a zoom
                            //map.dataProvider.zoomLevel = map.zoomLevel();
                            //map.dataProvider.zoomLatitude = map.dataProvider.zoomLatitude = map.zoomLatitude();
                            // map.dataProvider.zoomLongitude = map.dataProvider.zoomLongitude = map.zoomLongitude();
                            // map.validateNow(); //redraw the map with the new selection/colors.
                            map.write(to_plot);
                            mover_regiones() ; //mover regiones Peru y Colombia
                            seleccionar_mapa(selected_region);

					        }
					    }}
					],
					"zoomControl": {
						"zoomControlEnabled": false,
						"homeButtonEnabled": false,
						"panControlEnabled": false,
						"right": 38,
						"bottom": 30,
						"minZoomLevel": 0.25,
						"gridHeight": 100,
						"gridAlpha": 0.1,
						"gridBackgroundAlpha": 0,
						"gridColor": "#FFFFFF",
						"draggerAlpha": 1,
						"buttonCornerRadius": 2
					}
				});
	
	// mover las regiones de Colombia y Peru
	map.write(to_plot);
	mover_regiones();
	if(callback === undefined ){
	    return map;
	}else{
	    error = null;
	    callback(error, map);
	}

}

let peru_regions = [
			"path.amcharts-map-area.amcharts-map-area-PE-AMA",
			"path.amcharts-map-area.amcharts-map-area-PE-LOR",
			"path.amcharts-map-area.amcharts-map-area-PE-TUM",
			"path.amcharts-map-area.amcharts-map-area-PE-PIU",
			"path.amcharts-map-area.amcharts-map-area-PE-LAM",
			"path.amcharts-map-area.amcharts-map-area-PE-CAJ",
			"path.amcharts-map-area.amcharts-map-area-PE-SAM",
            "path.amcharts-map-area.amcharts-map-area-PE-LAM"
	
		];
	
let colombia_regions = [
		"path.amcharts-map-area.amcharts-map-area-CO-NAR", 
		"path.amcharts-map-area.amcharts-map-area-CO-AMA",
		"path.amcharts-map-area.amcharts-map-area-CO-PUT",
		"path.amcharts-map-area.amcharts-map-area-CO-CAQ",
		"path.amcharts-map-area.amcharts-map-area-CO-CAU",
		"path.amcharts-map-area.amcharts-map-area-CO-HUI"

	]; 
	
let cnel_regions = [
    "El Oro", "Guayas", "Santa Elena", "Manabí", "Esmeraldas",
	"Santo Domingo de los Tsáchilas",  "Los Ríos", "Bolívar", "Sucumbíos" ]



let ecuador_regions= [
	"Loja", "El Oro", "Guayas", "Santa Elena", "Manabí", "Esmeraldas", "Carchi", "Imbabura", "Pichincha", 
	"Santo Domingo de los Tsáchilas", "Cotopaxi", "Los Ríos", "Bolívar", "Tungurahua", "Chimborazo",
     "Bolívar", "Cañar", "Azuay", "Zamora-Chinchipe", "Sucumbíos", "Orellana", "Pastaza", "Napo",
    "Morona-Santiago", "Zamora-Chinchipe", "Galápagos"
	];

function is_in(member, lista){
	for(id in lista){
		if(member === lista[id]){
			return true;
		}
	}
	return false;
}

function mover_peru(){
	let scale_p = 1.11;
	var x_p = 496.5;
	var y_p = 71.3;
	var regions = d3.selectAll(".amcharts-map-area");
		for(id in peru_regions){
			regions.filter(peru_regions[id]).attr("transform", "translate(" + x_p  + "," + y_p + ") scale(" + scale_p +")");
		}
	return true;
}

function mover_colombia(){
	var scale_c = 1.115;
	var x_c = 492;
	var y_c = -508;
    var regions = d3.selectAll(".amcharts-map-area");
		for(id in colombia_regions){
			regions.filter(colombia_regions[id]).attr("transform", "translate(" + x_c  + "," + y_c + ") scale(" + scale_c +")");
		}
	return true;
}


function mover_galapagos(){
    var scale_c = 1;
    var x_c = 325;
    var y_c = -25;
    var regions = d3.selectAll(".amcharts-map-area");
    regions.filter("path.amcharts-map-area-EC-W").attr("transform", "translate(" + x_c  + "," + y_c + ") scale(" + scale_c +")");

    return true;
}


function mover_regiones(){

	// Mover regiones Peru y Colombia
    if(mover_peru() && mover_colombia() ){
		mover_galapagos();
	}
	// color de areas de otros países
        for (let i in map.dataProvider.areas ) {
                let area = map.dataProvider.areas[i];
                if (  is_in(area.title, ecuador_regions) === false) {
                    area.rollOverColorReal=otro_pais_color;
                }
         }

}	

let region_costa = [
    "El Oro", "Guayas", "Santa Elena", "Manabí", "Esmeraldas",
	"Santo Domingo de los Tsáchilas",  "Los Ríos"
];

let region_sierra =[
    "Loja", "Carchi", "Imbabura", "Pichincha", "Cotopaxi", "Bolívar", "Tungurahua", "Chimborazo",
    "Cañar", "Azuay"
];

let region_oriental =[
    "Zamora-Chinchipe", "Sucumbíos", "Orellana", "Pastaza", "Napo",
    "Morona-Santiago", "Zamora-Chinchipe"
];

let region_insular = ["Galápagos"];

function pintar_regiones(map, region_list, to_color){

    for (let i in map.dataProvider.areas ) {
	        let area = map.dataProvider.areas[i];
	        if (  is_in(area.title, region_list)=== true) {
				area.colorReal=to_color;
	        }
	 }
	 //map.write();
	 map.validateData();
	 mover_regiones();
	 return map;
}


function pintar_regiones_del_ecuador(map){
    // pintar region costa:
    map = pintar_regiones(map, region_costa, "rgba(100, 10, 10, 0.9)");
    // pintar region sierra:
    map = pintar_regiones(map, region_sierra, "#0e283b");
    // pintar region oriental
    map = pintar_regiones(map, region_oriental, "rgba(0, 74, 86, 0.9)");
    // pintar region insular
    map = pintar_regiones(map, region_insular, "rgba(200, 200, 100, 0.9)");

    return map;
}

function pintar_por_empresas(map){
    // pintar cnel
    map = pintar_regiones(map, cnel_regions, "rgb(100, 70, 125)");
    let emp = [];
    for(let id in ecuador_regions){
        if(!is_in(ecuador_regions[id], cnel_regions)){
            emp.push(ecuador_regions[id])
        }
    }
    map = pintar_regiones(map, emp, "rgb(78, 147, 197)");
    map = pintar_regiones(map, region_insular, "rgba(200, 200, 100, 0.9)");
    return map;
}


var scale = 1.115;
var x = 492;
var y = -508;
function load(){
    
		var regions = d3.selectAll(".amcharts-map-area");
		
		for(id in colombia_regions){
			console.log(colombia_regions[id]);
			regions.filter(colombia_regions[id]).attr("transform", "translate(" + x  + "," + y + ") scale(" + scale +")");
		}
		
}

function p(){
	x += 3;
	console.log(x)
	load();
}

function n(){
	x -= 3;
	console.log(x)
	load();
}

function py(){
	y += 3;
	console.log(y)
	load();
}

function ny(){
	y -= 3;
	console.log(y)
	load();
}

function ep(){
	scale += 0.005;
	console.log(scale)
	load();
}

function en(){
	scale -= 0.005;
	console.log(scale)
	load();
}
