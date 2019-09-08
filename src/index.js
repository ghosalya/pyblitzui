import React from 'react';
import ReactDOM from 'react-dom';
import Hero from './components/hero'
import Main from './components/main'
require('./assets/mystyles.scss');

class App extends React.Component {
    render() {
        return (
            <div>
                <Hero module="MyModule" />
                <Main className="container" />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
