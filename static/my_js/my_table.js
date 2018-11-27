
function create_table(tb_data, div, sortBy, filterCols){

	var table_plot;

	if( sortBy !== undefined && filterCols !== undefined){
	    table_plot = makeTable()
			.datum(tb_data)
			.sortBy(sortBy, true)
			.filterCols(filterCols);
    }
    else if( sortBy !== undefined ){
	    table_plot = makeTable()
			.datum(tb_data)
			.sortBy(sortBy, true);
    }
    else if( filterCols !== undefined){
    	table_plot = makeTable()
			.datum(tb_data)
			.filterCols(filterCols);
	}

	d3.select(div).call(table_plot);

	table_plot.on('select', function(data, on_off){
	  if(on_off){//if the data is highlighted
	      if(sortBy === undefined){
	          selected = data[Object.keys(data)[0]];
          }else{
	          selected = data[sortBy];
          }
		d3.select('#selected').text(
		  'Fila seleccionada: ' + selected
		);
	  }
	});


}