const fs        = require('fs');
const INTERVAL  = 2500;
const IMG_PATH  = './img/';
var photo_list  = fs.readdirSync(IMG_PATH);
var counter     = 0;

window.onload = function start() {
    slide();
}

function slide() {
    const contStyle = document.getElementById('container').style;
    setInterval(function() {
        document.getElementById('slide').src='./img/' + photo_list[counter];
        ++counter;
        photo_list = fs.readdirSync(IMG_PATH);
    }, INTERVAL);
    
}

