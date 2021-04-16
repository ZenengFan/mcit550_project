import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default class RecommendationsRow extends React.Component {
	constructor(props) {
		super(props);
	}

	render(movie,i) {
		return (
			<div key = {i} className="movieResults">
				<div className="title">{movie.title}</div>
				<div className="id">{movie.id}</div>
				<div className="rating">{movie.rating}</div>
				<div className="votes">{movie.vote_count}</div>
			</div>
		);
	}
}
