

function draw_ecuador_in_world( to_plot, callback){
	
	
	let map = AmCharts.makeChart( to_plot, {
					"type": "map",
					// "pathToImages": "http://www.amcharts.com/lib/3/images/",
					"creditsPosition": "bottom-right",
					"addClassNames": true,
					"fontSize": 15,
					"color": "black",
					"projection": "equirectangular",
					"backgroundAlpha": 1,
					// "backgroundColor": "rgba(37,97,142,1)",
					"backgroundColor": "black",
					"dataProvider": {
						"map": "worldHigh",
						"getAreasFromMap": true,
						"images": [],
						/*"images": [
							{
								"top": 40,
								"left": 60,
								"width": 80,
								"height": 40,
								"pixelMapperLogo": true,
								"imageURL": "http://pixelmap.amcharts.com/static/img/logo-black.svg",
								"url": "http://www.amcharts.com"
							}
						],*/
						"zoomLatitude": -2,
						"zoomLongitude": -85,
						"zoomLevel": 6.5,
						"areas": [
							{
								"id": "EC",
								"title": "Ecuador",
								"color": "rgba(255, 170, 0, 1)"
							}
						]
					},
					"balloon": {
						"horizontalPadding": 15,
						"borderAlpha": 0,
						"borderThickness": 1,
						"verticalPadding": 15
					},
					"areasSettings": {
						"color": "#0e283b",
						"outlineColor": "rgba(37,97,142,1)",
						"rollOverOutlineColor": "rgba(255,97,142,1)",
						"rollOverBrightness": 20,
						"selectedBrightness": 20,
						"selectable": true,
						"unlistedAreasAlpha": 0,
						"unlistedAreasOutlineAlpha": 0
					},
					"imagesSettings": {
						"alpha": 1,
						"color": "rgba(71,34,34,1)",
						"outlineAlpha": 0,
						"rollOverScale": 1.5,
						"rollOverColor": "rgba(37,97,142,1)",
						"selectedScale": 1.5,
						"rollOverOutlineAlpha": 0,
						"outlineColor": "rgba(37,97,142,1)",
						"rollOverBrightness": 10,
						"selectedBrightness": 80,
						"selectable": true
					},
					"linesSettings": {
						"color": "rgba(71,34,34,1)",
						"selectable": true,
						"rollOverBrightness": 20,
						"selectedBrightness": 20
					},
					"zoomControl": {
						"zoomControlEnabled": false,
						"homeButtonEnabled": false,
						"panControlEnabled": false,
						"right": 38,
						"bottom": 30,
						"minZoomLevel": 0.25,
						"gridHeight": 200,
						"gridAlpha": 0.1,
						"gridBackgroundAlpha": 0,
						"gridColor": "#FFFFFF",
						"draggerAlpha": 1,
						"buttonCornerRadius": 2
					},
					"listeners": [{
						"event": "clickMapObject",
						"method": function(event) {
							seleccionar_mapa(event.mapObject.title);
						}
					}]
				});
				
				let cities = [{
					"title": "Quito",
					"latitude": -0.2295,
					"longitude": -78.5243
				},{
					"title": "Guayaquil",
					"latitude": -2.1710,
					"longitude": -79.9224
					
				}];
				
				
			for(id in cities){
				city = new AmCharts.MapImage();
				city.title = cities[id].title;
				city.latitude = cities[id].latitude;
				city.longitude = cities[id].longitude;
				city.type = "hexagon";
				city.label = cities[id].title; 
				city.color = "rgba(153, 204, 255, 1)";
				city.labelColor = "white";
				city.chart = map;
				map.dataProvider.images.push(city);
				//city.validate();
			}
    map.validateNow();
	if(callback === undefined){
	    return map;
	}else{
	    callback(null, map);
	}


}

