import React, {	Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Amplify } from 'aws-amplify';
import { fetchAuthSession } from 'aws-amplify/auth';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

const apiId = process.env.REACT_APP_API_ID;
const stage = process.env.REACT_APP_API_STAGE;
const regionId = process.env.REACT_APP_REGION;
const clientId = process.env.REACT_APP_COGNITO_USER_POOL_CLIENT_ID;
const userPoolId = process.env.REACT_APP_COGNITO_USER_POOL_ID;
const cognitoDomainPref = process.env.REACT_APP_COGNITO_DOMAIN_PREFIX;
const cognitoDomain = `${cognitoDomainPref}.auth.${regionId}.amazoncognito.com`;
const apiGateway = `https://${apiId}.execute-api.${regionId}.amazonaws.com/${stage}`;

Amplify.configure({
  Auth: {
    Cognito: {
      region: regionId,
      userPoolId: userPoolId,
      userPoolClientId: clientId, // Changed from userPoolWebClientId
      loginWith: {
        oauth: {
          domain: cognitoDomain,
          scopes: ["email", "profile", "openid", "aws.cognito.signin.user.admin"],
          redirectSignIn: [process.env.REACT_APP_REDIRECT_SIGN_IN],
          redirectSignOut: [process.env.REACT_APP_REDIRECT_SIGN_OUT], 
          responseType: process.env.REACT_APP_OAUTH_RESPONSE_TYPE || "code", 
        }
      }
    }
  }
});

class AppContent extends Component {
    constructor(props) {
      super(props);
      this.state = {
            contacts: "",
            usernameClaims: "",
            usernameClaimsAuthorizer: ""
       };
    }
	componentDidMount() {

		fetchAuthSession()
			.then((res) => {
			    console.log("fetchAuthSession", res)
				// const jwtToken = res.getIdToken().getJwtToken();
        const jwtToken = res.tokens?.idToken?.toString()
				this.setState({
				    usernameClaims: res.tokens?.idToken?.payload?.['cognito:username']
				});
				fetch(apiGateway + '/demo', {
						headers: {
							'Authorization': 'Bearer ' + jwtToken
						}
					})
					.then(res => res.json())
					.then((data) => {
						console.log("demo.data",data)
						this.setState({
							contacts: (data.message),
							usernameClaimsAuthorizer: (data.input.requestContext.authorizer['cognito:username'])
						})
					})
					.catch(console.log)
			});
	}
	render() {
		return (
        <div className = "App" >
                    <header className = "App-header" >
                        <img src = {logo}
                        className = "App-logo"
                        alt = "logo" / >
                        <p >
                            Edit <code> src / App.js </code> and save to reload.
                        </p>
                         <div>
                            {cognitoDomain}
                         </div>
                         <div>
                            {apiGateway}
                         </div>
                         <div>
                             {this.state.contacts}
                         </div>
                         <div>
                              {this.state.usernameClaims} = {this.state.usernameClaimsAuthorizer}
                         </div>
                    </header>
			  </div>
		);
	}
}

function App() {
  return (
    <Authenticator>
      <AppContent />
    </Authenticator>
  );
}

export default App;
