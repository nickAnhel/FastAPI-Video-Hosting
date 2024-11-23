import { useState, useEffect, useContext } from "react";
import { observer } from "mobx-react-lite";
import "./Settings.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";

import SettingsService from "../../service/SettingsService";
import Loader from "../Loader/Loader";


function Settings() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);

    const [isLoading, setIsLoading] = useState(false);
    const [emailNotifications, setEmailNotifications] = useState(false);
    const [telegramNotifications, setTelegramNotifications] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const userSettings = await SettingsService.getSettings();
                setEmailNotifications(userSettings.data.enable_email_notifications);
                setTelegramNotifications(userSettings.data.enable_telegram_notifications);
            } catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, [store.user.emailNotifications, store.user.telegramNotifications])

    const handleSave = async () => {
        setIsLoading(true);
        try {
            const data = {
                enable_email_notifications: emailNotifications,
                enable_telegram_notifications: telegramNotifications,
            };
            await SettingsService.updateSettings(data);
        } catch (error) {
            console.log(error);
        }
        setIsLoading(false);

        alertsContext.addAlert({
            text: "Settings updated successfully",
            time: 2000,
            type: "success"
        })
    };

    return (
        <div className="settings">
            <section className="settings-section">
                <div className="section-header">
                    <h2 className="section-title">Notifications</h2>
                    <p className="section-description">Here you can change your notification settings</p>
                </div>

                <div className="section-body">
                    <label className="check-item" htmlFor="email-switch">
                        <input
                            className="check"
                            type="checkbox"
                            id="email-switch"
                            checked={emailNotifications}
                            onChange={(e) => setEmailNotifications(e.target.checked)}
                        />
                        <div className="toggle">
                            <span className="circle" />
                        </div>
                        <span className={emailNotifications ? "checked check-label" : "check-label"}>Enable email notifications</span>
                    </label>


                    <label className="check-item" htmlFor="telegram-switch">
                        <input
                            className="check"
                            type="checkbox"
                            id="telegram-switch"
                            checked={telegramNotifications}
                            onChange={(e) => setTelegramNotifications(e.target.checked)}
                        />
                        <div className="toggle">
                            <span className="circle" />
                        </div>
                        <span className={telegramNotifications ? "checked check-label" : "check-label"}>Enable telegram notifications</span>
                    </label>
                </div>
            </section>

            <button
                type="submit"
                className="save-button"
                onClick={handleSave}
                disabled={isLoading}
            >
                {isLoading ? <Loader /> : "Save"}
            </button>
        </div>
    )
}


export default observer(Settings)
