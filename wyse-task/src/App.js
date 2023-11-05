import "./App.css";
import { useState } from "react";
import SignInScreen from "./Screens/SignInScreen";
import { authentication } from "./firebase-config";
import HomeScreen from "./Screens/HomeScreen";
function App() {
  const [isSignedIn,setIsSignedIn] = useState(false);
  // update state when users signs in
  authentication.onAuthStateChanged((user)=>{
    console.log(user)
    if(user){
      setIsSignedIn(true);
    }
    else{
      setIsSignedIn(false);
    }
  })
 
  return (
    <div className="App">

      {isSignedIn === true?
        <HomeScreen/>
        :
        <SignInScreen/>
      }
    </div>
  );
}

export default App;
