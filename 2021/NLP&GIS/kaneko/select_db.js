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

//console.log(`SELECT * from spots WHERE(title LIKE '%${process.argv[2]}%');`)

connection.query(`SELECT * from spots WHERE(title LIKE '%${process.argv[2]}%');`, function (err, rows, fields) {
	if (err) { console.log('err: ' + err); } 

	// console.log('タイトル: ' + rows[0].title);
	// console.log('リード文: ' + rows[0].lead_sentence);
  // console.log('概要文: ' + rows[0].overview);
  // console.log('緯度経度: ' + rows[0].longitude_latitude);
  // console.log('住所: ' + rows[0].addr);
  // console.log('住所補足: ' + rows[0].note);
  console.log(rows)

});

connection.end();
