// _____________________________________________________________________________________________________
// General variables to be used in any script:
// !! Don´t change this general values !!
let margin = {
        top: 5,
        right: 5,
        bottom: 5,
        left: 5
};

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

