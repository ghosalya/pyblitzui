import React from 'react';
import FunctionBar from './functionbar'


class Panel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            functions: [
                {
                    name: 'No function detected.',
                    args: {}
                },
            ],
        }
    }

    componentDidMount() {
        fetch('/function/list')
            .then(res => res.json())
            .then(res => this.setState({
                functions: res.functions
            }))
    }

    renderFunctionBars() {
        var functionBars = this.state.functions.map(fn =>
            (<FunctionBar key={ fn.name } name={ fn.name } args={ fn.args } />)
        );
        return functionBars;
    }

    render() {
        var functionBars = this.renderFunctionBars();
        return (
            <div className="column section is-10">
                { functionBars }
            </div>
        );
    }
}

export default Panel
