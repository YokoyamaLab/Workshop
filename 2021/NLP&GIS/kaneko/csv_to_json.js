const fs = require('fs')
const csv = require('csv')
fs.createReadStream('./wikipedia_data/wikidata2_hand1.csv')
  .pipe(csv.parse({columns: true}, function(err,data){
    fs.writeFile('./wikipedia_data/wikipediadata2_hand.json',JSON.stringify(data),(err,data) =>{
      if(err)
        console.log(err);
      else
        console.log('ok');
    //console.log(JSON.stringify(data));
    });
}));
