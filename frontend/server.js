var express = require('express');
var cors = require('cors');
var session = require('express-session');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('views'));

app.use(session({
  secret: 'cis4375team11',
  resave: true,
  saveUninitialized: true
}))

app.use(cors());

// set the view engine to ejs
app.set('view engine', 'ejs');

function requireLogin(req, res, next) {
  if (req.session.loggedIn) {
    next();
  } else {
    res.redirect('/');
  }
}

// index page 
app.get('/', function(req, res) {
    res.render('pages/index')
});

// Overview page
app.get('/overview', requireLogin, function(req, res) {
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

// Sugar Land page
app.get('/sugarland', requireLogin, function(req, res) {
  axios.get('http://127.0.0.1:5000/sugarland')
  .then((response)=>{
    var data = response.data;

    res.render('pages/sugarland', {
      data: data
    })
  })    
});

// Update Quantity Process
app.post('/update_quantity', requireLogin, function(req, res) {
  var quantity = req.body.quantity;
  var id = req.body.id;
  var table = req.body.table;
  var origQuantities = req.body.origQuantities;
  var location;

  if (table === 'sugarInventory') {
    location = 'sugarland';
  } else {
    location = 'galleria';
  }

  // Make POST request to backend
  axios.post('http://127.0.0.1:5000/api/update_quantity', {
    id: id,
    quantity: quantity,
    table: table,
    origQuantities: origQuantities
  })
  .then((response) => {
    if (response.status === 200) {
      res.redirect(`/${location}`);
    } else {
      res.redirect('/overview');
    }
  })
  .catch((error) => {
    console.error(error);
  });
});

// Galleria page
app.get('/galleria', requireLogin, function(req, res) {
  axios.get('http://127.0.0.1:5000/galleria')
  .then((response)=>{
      var data = response.data;
      
      res.render('pages/galleria', {
          data: data
    })   
  })
});

// Edit Inventory page
app.get('/edit_inv', requireLogin, function(req, res) {
  axios.get('http://127.0.0.1:5000/edit_inv')
  .then((response)=>{
    var data = response.data;

    res.render('pages/edit_inv', {
      data: data
    })
  })
});

// Update inventory count page both locations
app.get('/update_inv/:location', requireLogin, function(req, res) {
  var location = req.params.location;
  var apiUrl;
  var table;

  if (location === 'sugarland') {
    apiUrl = 'http://127.0.0.1:5000/sugarland';
    table = 'sugarInventory';
  } else if (location === 'galleria') {
    apiUrl = 'http://127.0.0.1:5000/galleria';
    table = 'galloInventory';
  } else {
    res.redirect('/overview');
    return;
  }

  axios.get(apiUrl)
      .then((response) => {
          var data = response.data;

          res.render('pages/update_inv', {
              location: location,
              table: table,
              data: data
          });
      })
      .catch((error) => {
          console.error(error);
      });
});

// Add Inventory Process
app.post('/edit_productinv', requireLogin, function(req, res) {
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
    if (response.status === 200) {
      res.redirect('/edit_inv');
    } else {
      res.redirect('/overview');
    }
  })
  .catch((error) => {
    console.error(error);
  });
});

// Update Inventory Process
app.post('/update_productinv', requireLogin, function(req, res) {
  var currentItemName = req.body.currentItemName;
  var category = req.body.category;
  var itemName = req.body.itemName;
  var price = req.body.price;

  // Make POST request to backend
  axios.post('http://127.0.0.1:5000/api/update_inventory', {
    updateItem: currentItemName,
    category: category,
    itemName: itemName,
    price: price
  })
  .then((response) => {
    if (response.status === 200) {
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
      if (response.status === 200) {
        req.session.loggedIn = true;
        // Redirect to the overview page if login is successful
        res.redirect('/overview');
      } else {
        // Render the login page with an authentication failure message
        res.render('/', {
        });
      }
    })
    // Handle any error that occurred during the request
    .catch((error) => {
      console.error(error);
    });
  });

// Logout process
app.get('/logout', requireLogin, function(req, res) {
  req.session.destroy(function(err) {
    res.redirect('/');
  });
});

app.listen(8080);
console.log('Listening on port 8080');
