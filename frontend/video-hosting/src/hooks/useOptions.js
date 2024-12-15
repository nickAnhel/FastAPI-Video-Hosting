import { useState } from "react";


export default function useOptions() {
    const [options, setOptions] = useState([]);

    return {
        options,
        setOptions,
    }
}