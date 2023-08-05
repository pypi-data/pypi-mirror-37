
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '...' : this;
      };

function bindEvents() {
    const graph = 'graph'
    const gd = document.getElementById(graph);
    const btn_add = document.getElementById('add');
    const table = document.getElementById('info');
    const toggle_cell = document.getElementById('target-cell');
    var target_cell = 'ctc';

    const color = {
        'centroid': 'OrangeRed', 
        'ctc': 'Crimson', 
        'nuclei': 'LightSkyBlue', 
        '+': 'Orange', 
        'immune': 'ForestGreen'}

    // workaround: https://github.com/plotly/plotly.js/issues/2504 
    gd.on('plotly_click', (eventData) => {
        // toggle selection
        var g = eventData.points[0].data.legendgroup
        if (g == 'centroid')
            return
        var l = eventData.points[0].curveNumber;
        var c = eventData.points[0].data.line.color;
        g = (g == target_cell) ? 'nuclei' : target_cell;
        var update = {'line': {color: color[g]}, 'legendgroup': g};
        Plotly.restyle(graph, update, [l]);
    });

    gd.on('plotly_selected', (eventData) => {
        var x = eventData.lassoPoints.x.map(i => ~~i);
        var y = eventData.lassoPoints.y.map(j => ~~j);
        var m = uuidv4();
        x.push(x[0]);
        y.push(y[0]);
        Plotly.addTraces(graph, {
            showlegend: false,
            legendgroup: 'new',
            name: m.trunc(10),
            mode: 'lines',
            line: {'color': color['+']},
            x: x,
            y: y,
            customdata: [m],
            fill: 'toself',
            opacity: 0.3
        });
        Plotly.relayout(graph, { dragmode: 'pan' });
    });

    gd.on('plotly_afterplot', () => {
        // clear table content first
        table.innerHTML = '';
        // aggregate by legendgroup
        var groups = gd.data.reduce((count, cur) => {
            g = cur.legendgroup;
            if (g == 'centroid') { count[g] = cur.x.length; }
            else if (g in count) { count[g]++; }
            else { count[g] = 1; }
            return count;
        }, {});
        // iterate group as TR
        for (var g in groups) {
            if (groups[g] <= 1) { continue; }
            var row = table.insertRow(-1);
            row.insertCell(0).innerHTML = g.toUpperCase();
            row.insertCell(1).innerHTML = groups[g];
        }
    });

    btn_add.onclick = () => {
        Plotly.relayout(graph, { dragmode: 'lasso' });
    };

    toggle_cell.onchange = (eventData) => {
        // hack way to get value of React Component
        const value = eventData.target.id;
        target_cell = (value.includes("Tumor")) ? 'ctc' : 'immune';
    };
};

setTimeout(bindEvents, 2000);
