/**
 * Simply a simple little webserver so we can check if the other server pings us back in xs-search
 */

const express = require('express')
const app = express()

app.set("view engine", "ejs");

let currentQuery = "tjctf{"

app.get('/', (req, res) => {
  const target = req.query.target ?? "http://localhost:8080"
  const attacker = req.query.attacker ?? "http://localhost:8000"
  res.render('index', { target, attacker })
})

app.get('/set', (req, res) => {
  currentQuery = req.query.query
  console.log(currentQuery)
  res.send({ success: true })
})

app.get('/currentQuery', (req, res) => {
  res.send({ value: currentQuery })
})

app.get('/reset', (req, res) => {
  currentQuery = "tjctf{"
  res.send({ success: true })
})

app.listen(8000)
