import React, {	Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Amplify, { Auth } from 'aws-amplify';
import { withAuthenticator } from "aws-amplify-react";

const regionId = "{regionId}"
const userPoolId = "{userPoolId}"
const clientId = "{clientId}"
const cognitoDomain = "{cognitoDomain}.auth." + regionId + ".amazoncognito.com"
const apiGateway = "https://{apiId}.execute-api." + regionId + ".amazonaws.com/{stage}"

Amplify.configure({
	Auth: {
		"region": regionId,
		"userPoolId": userPoolId,
		"userPoolWebClientId": clientId,
		"mandatorySignIn": true,
		"oauth": {
			"domain": cognitoDomain,
			"scope": ["email", "profile", "openid", "aws.cognito.signin.user.admin"],
			"redirectSignIn": "http://localhost:3000/",
			"redirectSignOut": "http://localhost:3000/",
			"responseType": "token"
		}
	}
});

class App extends Component {
	componentDidMount() {
		Auth.currentSession()
			.then((res) => {
				const jwtToken = res.getIdToken().getJwtToken();
				fetch(apiGateway + '/demo', {
						headers: {
							'Authorization': 'Bearer ' + jwtToken
						}
					})
					.then(res => res.json())
					.then((data) => {
						console.log(data)
						this.setState({
							contacts: (data)
						})
					})
					.catch(console.log)
			});
	}
	render() {
		return ( <div className = "App" >
                    <header className = "App-header" >
                        <img src = {logo}
                        className = "App-logo"
                        alt = "logo" / >
                        <p >
                            Edit < code > src / App.js < /code> and save to reload.
                        </p>
                         <a className = "App-link"
                            href = "https://reactjs.org"
                            target = "_blank"
                            rel = "noopener noreferrer" >
                            Learn React
                        </a>
                    </header>
			</div>
		);
	}
}


export default withAuthenticator(App);

