import React from 'react';


class Sidebar extends React.Component {
    render() {
        return (
            <div className="column is-2 has-background-light">
                <p className="menu-label is-hidden-touch">Files</p>

                <li>
                    <ul> ./ </ul>
                    <ul> ./__init__.py </ul>
                </li>

            </div>
        );
    }
}

export default Sidebar
