import "./Alert.css"


function Alert({ alert }) {
    return (
        <div className={alert.type == "success" ? "alert" : "alert error"}>
            {alert.text}
        </div>
    )
}

export default Alert;