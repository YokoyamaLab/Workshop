var {Client} = require('pg');

var client = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'touristspot',
    password: 'yamashita',
    port: '5432'
})

client.connect()

const query = "SELECT title,lead,overview,latitude,longitude,spotaddress FROM wikidata WHERE title='秋葉原';"

// text: "SELECT title,lead,overview,latitude,longitude,spotaddress FROM wikidata WHERE title='秋葉原';"

client.query(query)
    .then(res=> console.log(res.rows))
    .catch(e=>console.error(e.stack))

