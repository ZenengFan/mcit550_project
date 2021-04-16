var config = require('./db-config.js');
var mysql = require('mysql');

config.connectionLimit = 10;
var connection = mysql.createPool(config);

/* -------------------------------------------------- */
/* ------------------- Route Handlers --------------- */
/* -------------------------------------------------- */


/* ---- Q1a (Dashboard) ---- */
function getPredicted(req, res) {
  var query = `
    select format(predicted_cases,0) as predicted_cases, state
  from predicted;
  `;
  connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
      console.log(rows);
      res.json(rows);
    }
  });
  
};


/* ---- Q1b (Dashboard) ---- */
function getTopInGenre(req, res) {
  var inputGenre = req.params.genre;
  var query = `
    select m.title, m.rating, m.vote_count 
    from movies m join genres g on m.id = g.movie_id
    where g.genre like '${inputGenre}'
    order by m.rating desc, vote_count desc
    limit 10;
  `;
  connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
      console.log(rows);
      res.json(rows);
    }
  });
};

/* ---- Q2 (Recommendations) ---- */
function getRecs(req, res) {
  var inputMovieName = req.params.movieName;
  var query = `
    with temp1 as(select * 
    from genres g join movies m on g.movie_id = m.id),

    temp3 as (select temp1.id from 
    temp1 where temp1.title like '${inputMovieName}'
    limit 1),

    temp2 as (select distinct temp1.genre from 
    temp1,temp3 where temp1.id = temp3.id)
 
    select distinct p0.title, p0.id, p0.rating, p0.vote_count 
    from temp1 p0, temp3
    where p0.id != temp3.id and (select count(distinct p1.genre)
    from temp1 p1
    where p1.id = p0.id and p1.genre in (select distinct temp1.genre from 
    temp1, temp3 where temp1.id = temp3.id)) = (select count(*) as num1 from temp2)
    order by p0.rating desc, p0.vote_count desc
    limit 5;
  `;
  connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
      console.log(rows);
      res.json(rows);
    }
  });
  
};

/* ---- (Best Genres) ---- */
function getDecades(req, res) {
	var query = `
    SELECT DISTINCT (FLOOR(year/10)*10) AS decade
    FROM (
      SELECT DISTINCT release_year as year
      FROM Movies
      ORDER BY release_year
    ) y
  `;
  connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
      console.log(rows);
      res.json(rows);
    }
  });
}

/* ---- Q3 (Best Genres) ---- */
function bestGenresPerDecade(req, res) {
  var inputDecade = req.params.decade;
  var query = `
    with temp1 as (select FLOOR(m.release_year/10)*10 as decade, g.genre as genre1, m.rating, m.id
    from genres g join movies m on g.movie_id = m.id),

    temp2 as (select distinct temp1.genre1 as genre2 from temp1),

    temp3 as (select * 
    from temp1 
    where temp1.decade = ${inputDecade}),

    temp4 as (select *
    from temp2 right join temp3 on temp2.genre2 = temp3.genre1
    union
    select *
    from temp2 left join temp3 on temp2.genre2 = temp3.genre1),

    temp5 as (select temp4.genre2 as genre, ifnull(temp4.rating,0) as rating
    from temp4)

    select temp5.genre, avg(temp5.rating) as avg_rating
    from temp5
    group by temp5.genre
    order by avg_rating desc, temp5.genre
  `;
  connection.query(query, function(err, rows, fields) {
    if (err) console.log(err);
    else {
      console.log(rows);
      res.json(rows);
    }
  });

};

// The exported functions, which can be accessed in index.js.
module.exports = {
	getPredicted: getPredicted,
	getTopInGenre: getTopInGenre,
	getRecs: getRecs,
	getDecades: getDecades,
  bestGenresPerDecade: bestGenresPerDecade
}