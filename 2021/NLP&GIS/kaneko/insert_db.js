const fs = require('fs')

jsonFile = './wikipedia_data/wikipediadata2_hand.json'

var wikipediaData = require(jsonFile);
//console.log(wikipediaData.length)
var mysqlSetting = require('./mysql_setting.json')

//console.log(mysqlSetting['password'])

const express = require('express')

// パッケージはmysqlではなくmysql2を使うと動く
//https://www.chuken-engineer.com/entry/2020/09/04/074216
const mysql = require('mysql2')

const app = express()

const connection = mysql.createConnection({
  host: 'localhost',
  user: mysqlSetting['user'],
  password: mysqlSetting['password'],
  database: 'spot_data'
});

connection.connect((err) => {
  if (err) {
    console.log('error connecting: ' + err.stack);
    return;
  }
  console.log('success');
});

for(var i = 0; i < wikipediaData.length; i++){
  title = wikipediaData[i]['タイトル']
  leadSentence = wikipediaData[i]['リード文']
  overview = wikipediaData[i]['概要文']
  idokeido = wikipediaData[i]['緯度経度']
  addr = wikipediaData[i]['住所']
  note = wikipediaData[i]['住所補足']
  title = "\'" + title + "\'"
  if(leadSentence == "")
    leadSentence = "NULL"
  else
    leadSentence = "\'" + leadSentence + "\'"
  if(overview == "None")
    overview = "NULL"
  else
    overview = "\'" + overview + "\'"
  if(idokeido == "None")
    idokeido = "NULL"
  else
    idokeido = "\'" + idokeido + "\'"
  if(addr == "None" || "ー")
    addr = "NULL"
  else
    addr = "\'" + addr + "\'"
  if(note == "")
    note = "NULL"
  else
    note = "\'" + note + "\'"
  
  console.log(`INSERT INTO spots(todofuken_id,title,lead_sentence,overview,longitude_latitude,addr,note) VALUES(13,${title},${leadSentence},${overview},${idokeido},${addr},${note});`)
  
  connection.query(`INSERT INTO spots(todofuken_id,title,lead_sentence,overview,longitude_latitude,addr,note) VALUES(13,${title},${leadSentence},${overview},${idokeido},${addr},${note});`, (err, results, fields) => {
      if (err) throw err;
  }); 
}

connection.end();
