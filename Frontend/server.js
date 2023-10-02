var express = require('express');
var app = express();





// set the view engine to ejs
app.set('view engine', 'ejs');

// index page 
// This page renders the login page. A variable 'attempt' is created and set to 'false'. This is used in the program later to see if the user has attempted to enter in data.
app.get('/', function(req, res) {
    res.render('pages/index')
});

// Login process
app.post('/process_login', function(req,res){
    var username = req.body.username;
    var password = req.body.password;

    if(username === 'user' && password === 'verysecurepassword')
    {   
        axios.get(`http://127.0.0.1:5000/api/testview`)
    }
    else
    {
        res.render('pages/index', {
            auth: false,
            attempt: true
        });    
    }
});


app.listen(8080);
console.log('Listening on port 8080');