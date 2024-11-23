import { useEffect, useState } from "react";


export default function useAlerts() {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const firstAlert = alerts[0];

        if (firstAlert) {
            const timer = setTimeout(() => {
                removeAlert(firstAlert.id)
            }, firstAlert?.time || 1000)

            return () => clearTimeout(timer)
        }

    })

    const removeAlert = (id) => {
        setAlerts(
            [...alerts].filter(alert => alert.id !== id)
        );
    }

    const addAlert = (alert) => {
        setAlerts(
            [...alerts, {
                id: (alerts.at(-1)?.id + 1) || 1,
                ...alert
            }]
        )
    }

    return {
        alerts,
        addAlert,
        removeAlert,
    }
}