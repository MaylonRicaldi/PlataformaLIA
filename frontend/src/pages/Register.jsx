import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
createUserWithEmailAndPassword
}
from "firebase/auth";

import { auth } from "../app/firebase";

import "./Auth.css";


export default function Register(){

const navigate=useNavigate()

const[email,setEmail]=useState("")
const[password,setPassword]=useState("")
const[loading,setLoading]=useState(false)



const registerUser=async(e)=>{

e.preventDefault()

setLoading(true)

try{

await createUserWithEmailAndPassword(
auth,
email,
password
)

alert(
"Usuario creado"
)

navigate("/")

}
catch(error){

alert(
error.message
)

}
finally{

setLoading(false)

}

}



return(

<div className="auth-page">

<form
onSubmit={registerUser}
className="auth-card"
>

<h1>
Crear Cuenta
</h1>

<input
type="email"
placeholder="Correo"
value={email}
onChange={(e)=>
setEmail(e.target.value)
}
/>


<input
type="password"
placeholder="Contraseña"
value={password}
onChange={(e)=>
setPassword(e.target.value)
}
/>


<button
disabled={loading}
>

{
loading
?
"Creando..."
:
"Registrarse"
}

</button>

</form>

</div>

)

}