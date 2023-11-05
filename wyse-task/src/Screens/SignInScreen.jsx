import { useState } from "react";
import { authentication } from "../firebase-config";
import { signInWithPopup, GoogleAuthProvider, signInWithCustomToken } from "firebase/auth";
const SignInScreen = ()=>{

    const [email,setEmail]=useState('');
    const [password,setPassword]=useState('');
    const [isRegistered,setIsRegistered]=useState(false);
    const [firstName,setFirstName]=useState('');
    const [lastName,setLastName]=useState('');
    const [error,setError]=useState('');
    /*
    const signIn = ()=>{
        const provider = new GoogleAuthProvider();
        console.log("google sign in");
        signInWithPopup(authentication, provider)
            .then((result) => {
            console.log(result);
            })
            .catch((error) => {
            console.log(error)
            });
    }
    */

    const registerUser = async () => {
      // if (email === '' || password === '') {
      //   setError('Email and password are required');
      //   return;
      // }
    
      try {
        const response = await fetch('http://127.0.0.1:8000/getData/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password, firstName, lastName })
        });
        const responseData = await response.json();
        if (responseData.message === 'User registered successfully') {
          setIsRegistered(true);
        }
        else if(responseData.error !== ''){
          console.log(error)
          setError(responseData.error)
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const login=()=>{
      setIsRegistered(true)
    }
    
    
    const loginUser = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/getData/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password})
          });
    
    
          const responseData = await response.json();
          // optional chaining based on our backen response
          const loginError=responseData?.error;
          if(loginError !== undefined){
            console.log(loginError)
            setError(loginError)
          }
          else{
            signInWithCustomToken(authentication, responseData.custom_token)
            .then((userCredential) => {
                const user = userCredential.user;
                console.log(user)
            })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.error('Error:', errorCode,errorMessage);
            });
          }
          
        } catch (error) {
          console.error('Error:', error);
        }
      };

      return (
        <div className="container">
            {!isRegistered ? (
                <div className="form-container">
                    
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Last Name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                    />
                    <button onClick={registerUser}>Register</button>
                    <button onClick={login}>Already have an account? Login</button>
                    <p>{error}</p>
                </div>
            ) : (
                <div className="form-container">
                    
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button onClick={loginUser}>Login</button>
                    <p className="error">{error}</p>
                </div>
            )}
        </div>
    );
}
export default SignInScreen;