import { createContext } from 'react';
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom';
import './index.css'

import App from './App.jsx'
import Store from './store/store';


const store = new Store();
export const Context = createContext({ store, });


createRoot(document.getElementById('root')).render(
  <Context.Provider value={{ store }}>
    <App />
  </Context.Provider>
)
