var express = require('express');

//MySQLのユーザー名とパスワードの設定ファイル
var mysqlSetting = require('./mysql_setting.json')

var app = express();

var http = require('http').Server(app);
const io = require('socket.io')(http);

const PORT = 8000;

const mysql = require('mysql2')

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

app.get('/' , function(req, res){
    res.sendFile(__dirname+'/index.html');
});

io.on('connection',function(socket){
    console.log('connection');
    socket.on('get_data',function(msg){
        getData(msg,socket)
    });
    socket.on('disconnect',function(){
        console.log('disconnect');
    });
});

http.listen(PORT, function(){
    console.log('server listening. Port:' + PORT);
});

function getData(msg,socket){
  connection.query(`SELECT * from spots WHERE(title LIKE '%${msg}%');`, function (err, rows, fields) {
	if (err) { console.log('err: ' + err); } 

    var data = rows[0]
    socket.emit('send_data', data);
});}
