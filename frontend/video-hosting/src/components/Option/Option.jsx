import "./Option.css"


function Option({ text, iconSrc, onClickHandler }) {
    return (
        <div className="option" onClick={onClickHandler}>
            <img src={iconSrc} alt={text} />
            <div>{text}</div>
        </div>
    )
}

export default Option;