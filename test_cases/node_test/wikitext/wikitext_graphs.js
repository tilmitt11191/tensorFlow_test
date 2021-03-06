
var router = require('express').Router();
var async = require('async');
var cytoscape = require('cytoscape');
var mysql = require('mysql');
var log = require('../utils/utils').getLogger();
log.debug("wikitext_graph.js start");
//var markovCluster = require('../lib/cytoscape.js-markov-cluster/cytoscape-markov-cluster.js');
//markovCluster( cytoscape ); // register extension
var regCose = require('cytoscape-cose-bilkent');
regCose( cytoscape ); // register extension


var start_node = 1;
var end_node = 10;
var relevancy = 15

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'alladmin',
  password : 'admin',
  database : 'wikitext'
});


function returnSuccess(res, data) {
  res.send({
    status: "success",
    data: data
  });
}

log.debug("path" + __dirname)
router.get('/data', function(req, res, next){
	log.debug("routes_graphs.js router.get('/data', function(){ start");
	var graph = [];
	async.waterfall([
		function(callback){
			getNodesFromMysql(callback, graph);
		},
		function(callback){
			getEdgesFromMysql(callback, graph);
		},
		/*function(callback){
			createGraph(callback, graph);
		},*/
/*		function(callback){
			var clusters = graph.elements().markovCluster({
				expandFactor: 2,        // affects time of computation and cluster granularity to some extent: M * M
				inflateFactor: 2,       // affects cluster granularity (the greater the value, the more clusters): M(i,j) / E(j)
				multFactor: 1,          // optional self loops for each node. Use a neutral value to improve cluster computations.
				maxIterations: 10,      // maximum number of iterations of the MCL algorithm in a single run
				attributes: [           // attributes/features used to group nodes, ie. similarity values between nodes
    			function(edge) {
						return edge.data('weight');
					}
					// ... and so on
				]
			});
			callback(null);
		},*/
		function(callback){
			log.debug("return graph. length: " + graph.length);
			//graph.forEach( function(el){
				//log.debug("el: " + el);
			//});
			returnSuccess(res, graph);
			//returnSuccess(res, sampleGraph);
		}
	]);
});

function getNodesFromMysql(callback, graph) {
	connection.query('SELECT * from nodes;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("node num: " + rows.length);
		log.debug("graph.length before add nodes: " + graph.length);
		rows.forEach( function(row) {
			if(start_node <= row.id && row.id < end_node){
				//edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
				//data = '{"data":' + edge + '}';
				log.debug("node[" + row.id + "]")
				data = {
					"data": {
						"id": Number(row.id)
					}
				}
				//graph.push(JSON.stringify(data,null,'\t'));
				graph.push(data);
			}
		});
		log.debug("graph.length after add nodes: " + graph.length);
		callback(null);
	});
}

function getEdgesFromMysql(callback, graph) {
	log.debug("getEdgesFromMysql(graph) start");
	log.debug("graph.length: " + graph.length)
	/*
	query = 'SELECT * from edges;';
	records = mysql.format(query);
	log.debug("edge num: " + records.length);
	callback(null);
	*/
	/*
	var query = connection.query('SELECT * from edges;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
	});
	log.debug("edge num: " + query.length);
	*/
	
	connection.query('SELECT * from edges;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("edge num: " + rows.length);
		log.debug("graph.length before add edges: " + graph.length);
		rows.forEach( function(row) {
			if(row.relevancy < relevancy &&
				start_node <= row.start && row.start < end_node &&
				start_node < row.end && row.end < end_node ){
				//edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
				//data = '{"data":' + edge + '}';
				log.debug("edge from[" + row.start + "] to [" + row.end + "], relevancy[" + row.relevancy + "]")
				data = {
					"data": {
						"id": Number(row.id),
						"source": Number(row.start),
						"target": Number(row.end)
					},
					"style": {
						'width': row.relevancy,
						'line-color': '#ccc',
						'target-arrow-color': '#ccc',
						'target-arrow-shape': 'triangle'
					}
				}
				//graph.push(JSON.stringify(data,null,'\t'));
				graph.push(data);
				log.debug("edge from[" + data.start + "] to [" + data.end + "], relevancy[" + data.relevancy + "]")
			}
		});
		//log.debug("graph.length after add edges: " + graph.length);
		callback(null);
	});
}

function createGraph(graph){

}

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
    //name: 'breadthfirst',
    //name: 'cose',
    //rows: 1
  }
}

var coseDefaultOptions = {
	name: 'cose-bilkent',
  // Called on `layoutready`
  ready: function () {
  },
  // Called on `layoutstop`
  stop: function () {
  },
  // number of ticks per frame; higher is faster but more jerky
  refresh: 30, 
  // Whether to fit the network view after when done
  fit: true,
  // Padding on fit
  padding: 10,
  // Padding for compounds
  paddingCompound: 15,
  // Whether to enable incremental mode
  randomize: true,
  // Node repulsion (non overlapping) multiplier
  nodeRepulsion: 4500,
  // Ideal edge (non nested) length
  idealEdgeLength: 50,
  // Divisor to compute edge forces
  edgeElasticity: 0.45,
  // Nesting factor (multiplier) to compute ideal edge length for nested edges
  nestingFactor: 0.1,
  // Gravity force (constant)
  gravity: 0.25,
  // Maximum number of iterations to perform
  numIter: 2500,
  // For enabling tiling
  tile: true,
  // Type of layout animation. The option set is {'during', 'end', false}
  animate: 'end',
  // Represents the amount of the vertical space to put between the zero degree members during the tiling operation(can also be a function)
  tilingPaddingVertical: 10,
  // Represents the amount of the horizontal space to put between the zero degree members during the tiling operation(can also be a function)
  tilingPaddingHorizontal: 10,
  // Gravity range (constant) for compounds
  gravityRangeCompound: 1.5,
  // Gravity force (constant) for compounds
  gravityCompound: 1.0,
  // Gravity range (constant)
  gravityRange: 3.8
};

module.exports = router;
