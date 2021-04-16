import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'

export default class DashboardMovieRow extends React.Component {
	constructor(props) {
		super(props);
	}

	/* ---- Q1b (Dashboard) ---- */
	/* Change the contents (NOT THE STRUCTURE) of the HTML elements to show a movie row. */
	render(movie,i) {
		return (
			<div key = {i} className="movie">
				<div className="state">{movie.state}</div>
				<div className="predicted_cases">{movie.predicted_cases}</div>
			</div>
		);
	}
}
