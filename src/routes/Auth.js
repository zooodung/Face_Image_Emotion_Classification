import { authService } from "../firebase";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { useState } from "react";


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
                    data = await createUserWithEmailAndPassword(authService, email, pw)
                } else {
                    // login
                    data = await signInWithEmailAndPassword(authService, email, pw)
                }
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