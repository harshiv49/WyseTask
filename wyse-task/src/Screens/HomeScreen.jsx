import { authentication } from "../firebase-config";
import { useRef, useState } from "react";
const HomeScreen=()=>{
  
    const [userName,setUserName]=useState('');
    const [lastName,setLastName]=useState('');
    const [firstName,setFirstName]=useState('');
    const [message,setMessage]=useState('');
    const tokenRef = useRef('');
    const logout = ()=>{
        authentication.signOut();
    }
   
    const getData = ()=>{
        authentication.onAuthStateChanged( async (user)=>{
            if(user){
                const uid=user?.uid;
                let token = await user.getIdToken();
                tokenRef.current=token;
                fetch(`http://127.0.0.1:8000/getData/${uid}`,{
                    headers:{
                        "Authorization":`Bearer ${token}`
                    }
                })
                .then((response)=>response.json())
                .then((JsonResponse)=>{
                    console.log(JsonResponse);
                })
            }
        })
    }
    console.log(tokenRef)
    const update=async () =>{
        console.log("tokenwa",tokenRef.current)
        try {
            const response = await fetch('http://127.0.0.1:8000/getData/update/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                "Authorization":`Bearer ${tokenRef.current}`
              },
              body: JSON.stringify({ firstName, lastName, userName })
            });
        
            const responseData = await response.json();
            console.log(responseData)
            if(responseData.message !== undefined){
                setMessage(responseData.message)
            }
            else{
                setMessage(responseData.error)
            }
          } catch (error) {
            console.error('Error:', error);
          }
    }

    return (
        <div className="container">
            <div className="card">
                <div className="form-container">
                    <input
                        type="text"
                        placeholder="Username"
                        value={userName}
                        onChange={(e) => setUserName(e.target.value)}
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
                    <button onClick={update}>Update</button>
                    <br/>
                    <button onClick={getData}>Get Data</button>
                    <br/>
                    <button onClick={logout}>Logout</button>
                    <br/>
                    <p className="message">{message}</p>
                </div>
            </div>
        </div>
    );
}
export default HomeScreen;