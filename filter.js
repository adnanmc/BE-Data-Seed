var jsonToCSV = require('json-to-csv');
var fs = require('fs');
var v = require('voca');

fs.readFile('./DATA/data.json', (err, json) => {
  let obj = JSON.parse(json);
  let filteredData = obj.filter((row) => {
      if (Number(row.STDudt) < Number(row.ETDudt) && v(row.OUTudt).trim() != "" && v(row.OFFudt).trim() != "" && v(row.ONudt).trim() != "" && v(row.INudt).trim() != "" && !v(row.tailNumber).trim().startsWith('-', 0)) {
        return row;
      }});
  console.log(filteredData);
  const fileName = './filtered_data/filtered.csv';
  jsonToCSV(filteredData, fileName)
    .then(() => {
      // success
      console.log('success');
    })
    .catch(error => {
      // handle error
      console.log(error);
    });
});
