import { useState, useEffect } from "react";
import "./SocialLink.css"


function SocialLink({ link }) {
    const [imgSrc, setImgSrc] = useState("");

    useEffect(() => {
        const wrapper = async () => {
            try {
                const domain = new URL(link).hostname;
                const faviconUrl = `https://www.google.com/s2/favicons?domain=${domain}&sz=48`;

                const img = new Image();
                img.src = faviconUrl;

                img.onload = () => {
                    if (img.naturalWidth >= 32 && img.naturalHeight >= 32) {
                        setImgSrc(faviconUrl);
                    } else {
                        setImgSrc("../../../../assets/link.svg")
                    }
                }

            } catch (e) {
                console.log(e);
            }
        }

        wrapper()
    }, [link])

    return (
        <a
            className="social-link"
            href={link}
            target="_blank">
            <img
                src={imgSrc}
                onError={() => {setImgSrc("../../../../assets/link.svg")}}
                alt={link}
            />
        </a>
    )
}

export default SocialLink;