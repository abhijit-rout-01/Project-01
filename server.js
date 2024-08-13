//required packages
const express = require("express");
const fetch = require("node-fetch");
const multer = require('multer');
const fs = require('fs');
//var jsdom = require("jsdom");
//var JSDOM = jsdom.JSDOM
require("dotenv").config();

//create the express server
const server = express();

//server port number
const PORT = process.env.PORT || 3000;

//set template engine
server.set("view engine","ejs");
var path = require('path');
const { title } = require("process");
server.use(express.static(path.join(__dirname, 'public')));

//needed to parse html data for POST request
server.use(express.urlencoded({
    extended:true
}))
server.use(express.json());

//OPERATIONS
server.get("/",(req,res)=>{
    res.render(__dirname+"/public/views/home.ejs");
});

server.get("/task1",(req,res)=>{
    res.render(__dirname+"/public/views/task1.ejs");
});

server.get("/task2",(req,res)=>{
    res.render(__dirname+"/public/views/task2.ejs");
});

server.post("/convert",async (req,res)=>{
    let videoID = req.body.videoID;
    let videoID1 = '';
    const len = videoID.length;
    let i=0;
    for(i=0;i<len;i++){
        if(videoID[i]==='='){
            i=i+1;
            break;
        }
    }
    while(i<len){
        videoID1 = videoID1+videoID[i];
        i++;
        if(videoID[i]==='&')
            break;
    }
    videoID = videoID1;
    //console.log(videoID);

    if(videoID===undefined || videoID==="" || videoID===null){
        return res.render(__dirname+"/public/views/task1.ejs",{success:false, message:"Please enter a valid url"});
    }
    else{
        console.log(1);
        const fetchAPI = await fetch('https://youtube-mp36.p.rapidapi.com/dl?id='+videoID, {
            "method" : "GET",
            "headers" : {
                "x-rapidapi-key" : process.env.API_KEY,
                "x-rapidapi-host" : process.env.API_HOST
            }
        });
        console.log(2);

        const fetchResponse = await fetchAPI.json();

        if(fetchResponse.status === "ok"){
            //check if song already there
            const file = path.join(__dirname,'public/css/task1/songs.json');
            let jsonData="";
            let song_source="";
            jsonData = await r(file);
            if(jsonData.includes(fetchResponse.title+'_'+videoID)){
                console.log(jsonData);
                song_source = "Song already taken, try another. Yet you can download it.";
            }
            else{
                let title_new="";
                const t = fetchResponse.title;
                let i=0;
                for(i=0;i<t.length;i++){
                    if(t[i]!='|'){
                        title_new=title_new+t[i];
                    }
                    else{
                        title_new=title_new+'_';
                    }
                }
                title_new=title_new+"_"+videoID;
                    
                console.log(4);
                try{song_source = title_new;
                    //call python to download audio
                    const spawner = require('child_process').spawn;
                    console.log(5);
                    const python_process = spawner('python',[__dirname+'public/python/MelSpec2.py',fetchResponse.link,fetchResponse.title,videoID]);
                    console.log(6);
                    python_process.stdout.on('data', (data)=>{
                        console.log(data);
                    });
                    console.log(7);}
                catch(err){
                    console.log(err);
                }
                r1(song_source);
            }
            function r(file){
                return new Promise((resolve,reject)=>{
                    fs.readFile(file, 'utf8', (err,data)=>{
                        if(err){
                            console.error("Error reading file",err);
                            reject("");
                        }
                        else{
                            resolve(JSON.stringify(data));
                        }
                    });
                })
            }
            function r1(){
                return res.render(__dirname+"/public/views/task1.ejs", {
                    success : true, 
                    song_title: fetchResponse.title, 
                    song_link : fetchResponse.link, 
                    song_source : song_source,
                });
            }     
        }
        else{
            return res.render(__dirname+"/public/views/task1.ejs", {success : false, message : fetchResponse.msg});
        }
    }
});

//json update
server.post('/update-json', (req, res) => {
    const updatedImages = req.body;
    console.log(1);
    // Save the updated JSON back to the file
    fs.writeFile(__dirname+"/public/css/task2/images.json", JSON.stringify(updatedImages, null, 4), (err) => {
        if (err) {
            console.error('Error writing to JSON file:', err);
            return res.status(500).send('Internal Server Error');
        }
        res.render(__dirname+"/public/views/task2.ejs");
    });
});

//imageSaveToBackend
const upload = multer({ dest: 'uploads/' });
server.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }

    // Move the file to a more appropriate location (optional)
    const tempPath = req.file.path;
    const targetPath = path.join(__dirname, 'public/uploads', req.file.originalname);

    fs.rename(tempPath, targetPath, err => {
        if (err) {
            return res.status(500).send('Error saving file.');
        }
        res.send('File uploaded successfully.');
    });
});

//start the server
server.listen(PORT, ()=>{
    console.log('Server started on port '+PORT);
})