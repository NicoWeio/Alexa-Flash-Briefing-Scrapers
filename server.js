var express = require('express');
var app = express();

const GOLEM = require('./golem');

app.get('/golem/', async (req, res) => {
  let r = await GOLEM();
  res.send(r);
});

app.listen(process.env.PORT || 8000);
