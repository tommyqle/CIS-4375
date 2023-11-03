var express = require('express');
var session = require('express-session');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');

app.use(bodyParser.urlencoded());
app.use(express.static('views'));

app.use(session({
  secret: 'testkey',
  resave: true,
  saveUninitialized: true
}))

// set the view engine to ejs
app.set('view engine', 'ejs');

// index page 
// This page renders the login page. A variable 'attempt' is created and set to 'false'. This is used in the program later to see if the user has attempted to enter in data.
app.get('/', function(req, res) {
    res.render('pages/index')
});

// Overview page
app.get('/overview', function(req, res) {
  if (req.session.loggedIn) {
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
  } else {
    res.redirect('/');
  }
});

// Sugar Land page
app.get('/sugarland', function(req, res) {
  if (req.session.loggedIn) {
    axios.get('http://127.0.0.1:5000/sugarland')
    .then((response)=>{
      var data = response.data;

      res.render('pages/sugarland', {
        data: data
      })
    })
  } else {
    res.redirect('/');
  }    
});

// Galleria page
app.get('/galleria', function(req, res) {
    axios.get('http://127.0.0.1:5000/galleria')
    .then((response)=>{
        var data = response.data;
        
        res.render('pages/galleria', {
            data: data
      })   
    })
});

// Edit Inventory page
app.get('/edit_inv', function(req, res) {
  if (req.session.loggedIn) {
    axios.get('http://127.0.0.1:5000/edit_inv')
    .then((response)=>{
      var data = response.data;

      res.render('pages/edit_inv', {
        data: data
      })
    })
  } else {
    res.redirect('/');
  }    
});

// Edit Inventory Process
app.post('/edit_productinv', function(req, res) {
  var category = req.body.category;
  var itemName = req.body.itemName;
  var price = req.body.price;

  // Make POST request to backend
  axios.post('http://127.0.0.1:5000/api/add_inventory', {
    category: category,
    itemName: itemName,
    price: price
  })
  .then((response) => {
    var result = response.data
    if (result === 'Successfully added!') {
      res.redirect('/edit_inv');
    } else {
      res.redirect('/overview');
    }
  })
  .catch((error) => {
    console.error(error);
  });
});

// Login process
app.post('/process_login', function(req, res) {
    var username = req.body.username;
    var password = req.body.password;
  
    // Make a POST request to backend
    axios.post('http://127.0.0.1:5000/api/login', {
      username: username,
      password: password
    })
    .then((response) => {
      var result = response.data;
      
      if (result === 'SUCCESS!') {
        req.session.loggedIn = true;
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
    // Handle any error that occurred during the request
    .catch((error) => {
      console.error(error);
    });
  });

app.listen(8080);
console.log('Listening on port 8080');