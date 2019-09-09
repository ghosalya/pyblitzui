import React from 'react';


class FunctionBar extends React.Component {
    // expects props.name and props.arg

    constructor(props) {
        super(props);

        this.state = {
            input: {},
            inputHandler: this.getInputHandler(props.args),
            output: null,
        }

        Object.keys(props.args).forEach((key, index) => {
            this.state.inputHandler[key] = this.state.inputHandler[key].bind(this)
        })
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    getInputHandler(args) {
        var handlerFns = {}
        Object.keys(args).forEach((key, index) => {
            var handlerFn = function (event) {
                // console.log(key, event.target.value)
                var newState = this.state
                newState.input[key] = event.target.value
                this.setState(newState)
            }
            handlerFns[key] = handlerFn
        })
        return handlerFns
    }

    handleSubmit(event) {
        console.log(this.state.input);
        event.preventDefault()
        fetch("/function/call/" + this.props.name, {
            method: 'post',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(this.state.input),
        }).then(res => res.json())
          .then(res => this.setState({
              output: res.output
          }))
    }

    renderOutput() {
        if(this.state.output == null) {
            return (<div className="is-divider" data-content="Output (Empty)"></div>)
        } else {
            return (
                <div className="section">
                    <div className="is-divider" data-content="Output"></div>
                    <div className="section has-background-white-ter">
                        { this.state.output }
                    </div>
                </div>
            )
        }
    }

    render() {
        var argsForm = Object.keys(this.props.args).map((key, index) => (
            <div  className="columns is-vcentered">
                <div className="column is-2 has-text-right"> { key } : </div>
                <div className="column is-10">
                    <input
                        className="input"
                        type="text"
                        placeholder={ this.props.args[key] }
                        value={ this.state.input[key] }
                        onChange={ this.state.inputHandler[key] }
                    ></input>
                </div>
            </div>
          ))

        return (
            <div className="box">
                <h2 className="subtitle"> { this.props.name } </h2>
                <form onSubmit={ this.handleSubmit} >
                    { argsForm }
                    <input className="button" type="submit" value="Run Function"></input>
                </form>
                { this.renderOutput() }
            </div>
        );
    }
}

export default FunctionBar
