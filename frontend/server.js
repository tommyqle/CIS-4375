var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');

app.use(bodyParser.urlencoded());
app.use(express.static('views'));

// set the view engine to ejs
app.set('view engine', 'ejs');

// index page 
// This page renders the login page. A variable 'attempt' is created and set to 'false'. This is used in the program later to see if the user has attempted to enter in data.
app.get('/', function(req, res) {
    res.render('pages/index')
});

app.get('/overview', function(req, res) {
    axios.get('http://127.0.0.1:5000/sugarland')
    .then((response)=>{
        var sugar_data = response.data;
        axios.get('http://127.0.0.1:5000/galleria')
        .then((response)=>{
          var galleria_data = response.data;
          res.render('pages/overview', {
            sugar_data: sugar_data,
            galleria_data: galleria_data
        });
    });
  });
});

app.get('/sugarland', function(req, res) {
    axios.get('http://127.0.0.1:5000/sugarland')
    .then((response)=>{
        var data = response.data;
        
        res.render('pages/sugarland', {
            data: data
    })
    
    })
});

/* TESTING */
app.get('/sugarland_update', function(req, res) {
    res.render('pages/sugarland_update')
});


app.get('/galleria', function(req, res) {
    axios.get('http://127.0.0.1:5000/galleria')
    .then((response)=>{
        var data = response.data;
        
        res.render('pages/galleria', {
            data: data
    })
    
    })
});

/*
app.get('/sugarland', function(req, res) {
    axios.get('http://127.0.0.1:5000/sugarland')
    .then((response)=>{
        var data = response.data;
        
        res.render('pages/sugarland', {
            data: data
    })
    
    })
});

app.get('/montrose', function(req, res) {
    axios.get('http://127.0.0.1:5000/montrose')
    .then((response)=>{
        var data = response.data;
        
        res.render('pages/montrose', {
            data: data
    })
    
    })
});
*/
// Login process
app.post('/process_login', function(req, res) {
    var username = req.body.username;
    var password = req.body.password;
  
    // Make a POST request to your Flask backend
    axios.post('http://127.0.0.1:5000/api/login', {
      username: username,
      password: password
    })
    .then((response) => {
      var result = response.data;
      
      if (result === 'SUCCESS!') {
        // Redirect to the overview page if login is successful
        res.redirect('/overview');
      } else {
        // Render the login page with an authentication failure message
        res.render('pages/index', {
          auth: false,
          attempt: true
        });
      }
    })
    .catch((error) => {
      console.error(error);
      // Handle any error that occurred during the request
    });
  });

// app.post('/process_login', function(req,res){
//     var username = req.body.username;
//     var password = req.body.password;

//     if(username === 'user' && password === 'verysecurepassword')
//     {   
//         axios.get(`http://127.0.0.1:5000/api/inventory`)
//     }
//     else
//     {
//         res.render('pages/overview', {
//             auth: false,
//             attempt: true
//         });    
//     }
// });


app.listen(8080);
console.log('Listening on port 8080');