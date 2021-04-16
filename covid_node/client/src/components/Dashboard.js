import React from 'react';
import '../style/Dashboard.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import PageNavbar from './PageNavbar';
import GenreButton from './GenreButton';
import DashboardMovieRow from './DashboardMovieRow';

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    // The state maintained by this React Component. This component maintains the list of genres,
    // and a list of movies for a specified genre.
    this.state = {
      posts: []
    }

    //this.showMovies = this.showMovies.bind(this);
  }

  // React function that is called when the page load.
  componentDidMount() {
    console.log('I was triggered during componentDidMount')
    // Send an HTTP request to the server.
    fetch("http://localhost:8081/genres",
    {
      method: 'GET' // The type of HTTP request.
    }).then(res => {
      // Convert the response data to a JSON.
      return res.json();
    }).then(posts => {
        this.setState({posts});
      }).then(err => {
      // Print the error if there is one.
      console.log(err);
    })}
    
    //.then(genreList => {
      //if (!genreList) return;
      // Map each genreObj in genreList to an HTML element:
      // A button which triggers the showMovies function for each genre.
      //let genreDivs = genreList.map((genreObj, i) =>
      //<GenreButton id={"button-" + genreObj.genre} onClick={() => this.showMovies(genreObj.genre)} genre={genreObj.genre} />
      //);

      

      // Set the state of the genres list to the value returned by the HTTP response from the server.
      //this.setState({
        //genres: genreDivs
      //});
    //}, err => {
      // Print the error if there is one.
      //console.log(err);
    //});



  /* ---- Q1b (Dashboard) ---- */
  /* Set this.state.movies to a list of <DashboardMovieRow />'s. */
  
  render() {
    return (
      <div>
        <ul>
          {this.state.posts.map(post => (
            <p>
              <li>predict cases: {post.predicted_cases}</li>
              <li>state: {post.state}</li>
            </p>
          ))}
          </ul>
      </div>
    );
  }
}
