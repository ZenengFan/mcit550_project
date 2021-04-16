import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default class BestGenreRow extends React.Component {
	constructor(props) {
		super(props);
	}

	render(genre,i) {
		return (
			<div key = {i} className="movieResults">
				<div className="genre">{genre.genre}</div>
				<div className="rating">{genre.avg_rating}</div>
			</div>
		);
	}
}
