import { initializeApp } from "firebase/app";
import { getAuth} from "firebase/auth";
const firebaseConfig = {
    apiKey: "AIzaSyDuWgkRDQeX6NfAR287ur65BCoAJcsexbU",
    authDomain: "wysetask.firebaseapp.com",
    projectId: "wysetask",
    storageBucket: "wysetask.appspot.com",
    messagingSenderId: "137755005014",
    appId: "1:137755005014:web:e05151a1ab1504f7d4abf7"
  };

const app = initializeApp(firebaseConfig); 
export const authentication =getAuth(app);

