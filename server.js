var express = require('express');
var app = express();

const GOLEM = require('./golem');

app.get('/golem/', async (req, res) => {
  res.json((await GOLEM()));
});

app.listen(process.env.PORT || 8000);
