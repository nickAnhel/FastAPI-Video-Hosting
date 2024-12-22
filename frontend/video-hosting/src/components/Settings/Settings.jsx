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
                    <label
                        className={store.user.is_verified_email ? "check-item" : "disabled check-item"}
                        htmlFor="email-switch"
                    >
                        <input
                            className="check"
                            type="checkbox"
                            id="email-switch"
                            checked={emailNotifications}
                            onChange={(e) => setEmailNotifications(e.target.checked)}
                            disabled={!store.user.is_verified_email}
                        />
                        <div
                            className={store.user.is_verified_email ? "toggle" : "disabled toggle"}
                        >
                            <span className="circle" />
                        </div>

                        <span className={emailNotifications ? "checked check-label" : "check-label"}>Enable email notifications</span>

                        {
                            !store.user.is_verified_email &&
                            <span className="error">Please verify your email</span>
                        }
                    </label>


                    <label
                        className={store.user.is_verified_telegram ? "check-item" : "disabled check-item"}
                        htmlFor="telegram-switch"
                    >
                        <input
                            className="check"
                            type="checkbox"
                            id="telegram-switch"
                            checked={telegramNotifications}
                            onChange={(e) => setTelegramNotifications(e.target.checked)}
                            disabled={!store.user.is_verified_telegram}
                        />
                        <div
                            className={store.user.is_verified_telegram ? "toggle" : "disabled toggle"}
                        >
                            <span className="circle" />
                        </div>
                        <span className={telegramNotifications ? "checked check-label" : "check-label"}>Enable telegram notifications</span>

                        {
                            store.user.telegram_username != null ?
                                !store.user.is_verified_telegram ?
                                    <span className="error">Please verify your telegram</span>
                                    : null
                                : <span className="error">Please enter and verify your telegram</span>
                        }
                    </label>

                </div>
            </section>

            <button
                type="submit"
                className="save-button"
                onClick={handleSave}
                disabled={
                    isLoading ||
                    (
                        !store.user.is_verified_telegram &&
                        !store.user.is_verified_email
                    )
                }
            >
                {isLoading ? <Loader /> : "Save"}
            </button>
        </div>
    )
}


export default observer(Settings)
