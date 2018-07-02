const fs = require('fs-extra');
const v = require('voca');
const moment = require('moment');
const config = require('./config.json');


let env = config.env;
let targetDate = moment(config.targetDate, 'MM/DD/YYYY').format('DDMMMYY').toString().toUpperCase();
let previousDate = moment(config.targetDate, 'MM/DD/YYYY').add(-1, 'days').format('DDMMMYY').toString().toUpperCase();
let nextDate = moment(config.targetDate, 'MM/DD/YYYY').add(1, 'days').format('DDMMMYY').toString().toUpperCase();
let stg1DropLocation = '//gscfile01/SharedFile/QA_MVC/STG1/adh_receive';
let stg1ReceiveLocation = '//gscfile01/SharedFile/QA_MVC/STG1/adh_send';
let stg2DropLocation = '//gscfile01/SharedFile/QA_MVC/STG2/adh_receive';
let stg2ReceiveLocation = '//gscfile01/SharedFile/QA_MVC/STG2/adh_send';
let stg3DropLocation = '//gscfile01/SharedFile/QA_MVC/STG3/adh_receive';
let stg3ReceiveLocation = '//gscfile01/SharedFile/QA_MVC/STG3/adh_send';
let testLocation = './test';

let step1_OOOI_previousDay = async (env, date, location) => {
    try {
        let dropLocation = testLocation;
    let fileName = 'OOOI_Previous_Day.txt';
    let text = `ADH015_${date}TIMP0100000`;
    // if (env == 'stg1') {
    //     dropLocation = stg1DropLocation;
    // } else if (env =='stg2') {
    //     dropLocation = stg2DropLocation;
    // } else if (env =='stg3') {
    //     dropLocation = stg2DropLocation;
    // }

    await fs.writeFile(`${dropLocation}/${fileName}`, text).then((err) => {
        if (err) {
           console.log(err);
           return err;
        } else {
            console.log('step1 success');
        }
    });
    } catch (error) {
        console.log(error);
    } 
};



step1_OOOI_previousDay(env, previousDate, stg1DropLocation);