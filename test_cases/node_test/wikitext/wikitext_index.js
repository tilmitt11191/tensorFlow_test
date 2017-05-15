var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('../wikitext/wikitext_index', { projectTitle: "wikitext", pageTitle: "wikitext"});
});

module.exports = router;
