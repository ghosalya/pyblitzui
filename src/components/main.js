import React from 'react';
import Sidebar from './sidebar'
import Panel from './panel'


class Main extends React.Component {
    render() {
        return (
            <div className="container">
                <div className="section columns">
                    <Sidebar />
                    <Panel />
                </div>
            </div>
        );
    }
}

export default Main
