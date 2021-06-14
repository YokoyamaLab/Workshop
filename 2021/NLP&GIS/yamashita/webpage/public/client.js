var socket = window.io();
var userID;

// 最初の接続時にIDを受け取る
socket.on('initial',ID=>{
    userID = ID;
    console.log("userID="+userID);
});

// 結果を受け取る
socket.on('result',geoData=>{
    document.getElementById('title').innerHTML = geoData.title;
    document.getElementById('lead').innerHTML = geoData.lead;
    document.getElementById('overview').innerHTML = geoData.overview;
    document.getElementById('address').innerHTML = geoData.spotaddress;
    document.getElementById('latitude').innerHTML = "緯度:  " + geoData.latitude.toPrecision([5]);
    document.getElementById('longitude').innerHTML = "経度:  " + geoData.longitude.toPrecision([6]);
    document.getElementById('wordcloud').src = "img/"+geoData.title+"/TFIDF.png";
});

function searchSpot(){
    var spotName;
    spotName = document.getElementById("textbox").value;

    var sendData = {
        id: userID,
        name: spotName
    };

    socket.emit("getSpotname",sendData);
}
