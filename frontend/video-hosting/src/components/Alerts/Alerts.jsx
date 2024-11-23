import "./Alerts.css"

import Alert from "../Alert/Alert"


function Alerts({ alerts }) {
    return (
        <div className="alerts">
            {
                alerts && alerts.map((alert) => {
                    return <Alert key={alert.id} alert={alert}/>
                })
            }
        </div>
    )
}

export default Alerts;