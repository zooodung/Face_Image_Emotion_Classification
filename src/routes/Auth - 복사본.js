// import { authService } from "../firebase";
import { firebase, initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { useState } from "react";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_API_KEY,
  authDomain: process.env.REACT_APP_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_PROJECT_ID,
  storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_APP_ID,
  measurementId: process.env.REACT_APP_MEASUREMENT_ID
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const Auth = () => {
    const [email, setEmail] = useState("")
    const [pw, setPw] = useState("")
    const [newAccount, setNewAccount] = useState(true)

    const onChange = (event) => {
        const {
            target: { name, value },
        } = event;
        if (name === "email") {
            setEmail(value)
        } else if (name === "pw") {
            setPw(value)
        }
    };

    const onSubmit = async (event) => {
        event.preventDefault()
            try {
                let data
                if (newAccount) {
                    // create new account
                    console.log(email + pw+"@1")
                    data = await createUserWithEmailAndPassword(auth, email, pw)
                } else {
                    // login
                    console.log(email + pw+"@2")
                    data = await signInWithEmailAndPassword(auth, email, pw)
                }
                console.log(data);
            }  catch (error) {
                console.log(error);
            }
    };

    return (
        <div>
            <form onSubmit={onSubmit}>
                <input
                    name="email" 
                    type="email"
                    placeholder="Email"
                    required
                    value={email}
                    onChange={onChange}
                />
                <input
                    name="pw"
                    type="password"
                    placeholder="Password"
                    required
                    value={pw}
                    onChange={onChange}
                />
                <input type="submit" value={newAccount ? "Create Account" : "Log In"} />
            </form>
            <div>
                <button>Continue with Google</button>
                <button>Continue with Github</button>
            </div>
        </div>
    )
}

export default Auth;