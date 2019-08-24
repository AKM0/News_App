import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

import "normalize.css/normalize.css";
import "@blueprintjs/core/lib/css/blueprint.css"

ReactDOM.render(<App />, document.getElementById('root'));

serviceWorker.unregister();
