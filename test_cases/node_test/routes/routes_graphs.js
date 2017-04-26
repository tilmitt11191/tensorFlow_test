

var router = require('express').Router();
var async = require('async');
var cytoscape = require('cytoscape');
var mysql = require('mysql');
var log = require('../utils/utils').getLogger();

function returnSuccess(res, data) {
  res.send({
    status: "success",
    data: data
  });
}

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'alladmin',
  password : 'admin',
  database : 'mnist'
});

var graph = [];
var start_node = 1198;
var end_node = 1212;
router.get('/test', function(req, res, next){
	log.debug("routes_graphs.js router.post('/test', function(){ start");
	graph = [];
	async.waterfall([
		function(callback){
			for(var i = start_node; i < end_node; i++){
				data = {
					"data": {
						"id": i,
					},
					"style": {
						'width': '28px',
						'height': '28px',
						'background-image': "./images/" + i + ".png",
						'background-width' : "100%",
						'background-height' : "100%",
						'backgroud-fit': 'contain'
					}
				}
				graph.push(data);
			}

			log.debug("graph.length after add nodes: " + graph.length);
			callback(null);
		},
		function(callback){
			connection.query('SELECT * from edges;', function (err, rows, fields) {
				if (err) { console.log('err: ' + err); }
				log.debug("edge num: " + rows.length);
				log.debug("graph.length before add edges: " + graph.length);
				rows.forEach( function(row) {
					if(row.relevancy > 3 && start_node <= row.start && row.start < end_node && start_node < row.end && row.end <=end_node ){
						//edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
						//data = '{"data":' + edge + '}';
						data = {
							"data": {
								"id": row.id,
								"source": row.start,
								"target": row.end
							}
						}
						//graph.push(JSON.stringify(data,null,'\t'));
						graph.push(data);
					}
				});
				//log.debug("graph.length after add edges: " + graph.length);
				callback(null);
			});
		},
		function(callback){
			log.debug("graph.length before return: " + graph.length);
			graph.forEach( function(el){
				log.debug("el: " + el);
			});
			returnSuccess(res, graph);
			//returnSuccess(res, sampleGraph);
		}
	]);
});




function convertFromMySQLRecordsToCytoscape(graph) {
	log.debug("convertFromMySQLRecordsToCytoscape() start");
	connection.query('SELECT * from papers;', function (err, rows, fields, graph) {
		if (err) { console.log('err: ' + err); }
		log.debug("node num: " + rows.length);
		/*
		rows.forEach( function(row) {
			node = {"id": row.id};
			data = {"data": node};
			//log.debug("graph.push(" + JSON.stringify(data,null,'\t') + ")")
			graph.push(data);
		});
		log.debug("graph.length after add nodes: " + graph.length);
		*/
	});
	
	connection.query('SELECT * from edges;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("edge num: " + rows.length);
		/*rows.forEach( function(row) {
			if(row.relevancy > 1){
				edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
				data = '{"data":' + edge + '}';
				graph.push(data);
			}
		});*/
		//log.debug("graph.length after add edges: " + graph.length);
	});

	log.debug("graph.length method finished: " + graph.length);
	return graph;
	//return sampleGraph;
}


var sampleGraph = {
 elements: [ // list of graph elements to start with
    { // node a
      data: { id: 'x' }
    },
    { // node b
      data: { id: 'y' }
    },
    { // edge ab
      data: { id: 'xy', source: 'x', target: 'y' }
    }
  ],

  style: [ // the stylesheet for the graph
    {
      selector: 'node',
      style: {
        'background-color': '#666',
        'label': 'data(id)'
      }
    },

    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle'
      }
    }
  ],

  layout: {
    //name: 'grid',
    //name: 'random',
    //name: 'concentric',
    name: 'breadthfirst',
    //name: 'cose',
    rows: 1
  }
}


module.exports = router;