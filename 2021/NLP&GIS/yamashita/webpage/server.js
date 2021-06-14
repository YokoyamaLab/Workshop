// モジュール
const http     = require('http');
const express  = require('express');
const socketIO = require('socket.io');
const {Client} = require('pg');

// オブジェクト
const app = express();
const server = http.Server(app);
const io = socketIO(server);

// 定数
const PORT = 5500;
var queryBase1 = "SELECT title,lead,overview,latitude,longitude,spotaddress FROM wikidata WHERE title='";
var queryBase2 = "';";

// データベース
// 設定
var client = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'touristspot',
    password: 'yamashita',
    port: '5432'
})
// 接続
client.connect()

server.listen(PORT,()=>{
    console.log('server starts on port: %d',PORT);
    app.use(express.static(__dirname+'/public'));
});

io.on('connection',socket=>{

    userID = socket.id;
    io.to(userID).emit('initial',userID)

    socket.on('getSpotname',receiveData=>{
        console.log(receiveData.id + ":" + receiveData.name);
        querySpot = queryBase1 + receiveData.name + queryBase2;
        console.log(querySpot);
        client.query(querySpot, (err, res) => {
            if(err){
                console.log('Not Found');
            } else {
                console.log(res.rows[0].title + ' found');
                io.to(receiveData.id).emit('result',res.rows[0]);
            }
        });
    });

});

