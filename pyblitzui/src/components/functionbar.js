import React from 'react';


class FunctionBar extends React.Component {
    // expects props.name and props.arg

    constructor(props) {
        super(props);

        this.state = {
            input: {},
            inputHandler: this.getInputHandler(props.args),
            output: null,
            logs: null,
        }

        Object.keys(props.args).forEach((key, index) => {
            this.state.inputHandler[key] = this.state.inputHandler[key].bind(this)
        })
        this.handleSubmit = this.handleSubmit.bind(this)
        this.refreshLogs = this.refreshLogs.bind(this)
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
        this.setState({
            call_id: null,
            output: null,
            error: null,
            logs: null,
        })
        console.log(this.state.input);
        event.preventDefault()
        fetch("/function/call/" + this.props.name, {
            method: 'post',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(this.state.input),
        }).then(res => res.json())
          .then(res => this.setState({
              error: res.error,
              call_id: res.call_id,
          }))
          .then(res =>
            this.periodicFetch = setInterval(this.refreshLogs, 500)
          )
    }

    refreshLogs() {
        fetch("/function/logs/" + this.state.call_id)
          .then(res => res.json())
          .then(res => this.setState({
              logs: res.logs,
              output: res.output,
          }))
        if (this.state.output != null) {
            clearInterval(this.periodicFetch)
        }
    }

    renderLogs() {
        if (this.state.logs != null) {
            return this.state.logs.split('\n').map((item, i) => {
                return (<p>{item}</p>)
            })
        } else {
            return []
        }
    }

    renderOutput() {
        if(this.state.output != null) {
            return (
                <div className="section">
                    <div className="is-divider" data-content="Output"></div>
                    <div className="section has-background-white-ter">
                        { this.state.output }
                    </div>
                </div>
            )
        } else if (this.state.error != null) {
            return (
                <div className="section">
                    <div className="is-divider" data-content="ERROR"></div>
                    <div className="section has-background-danger">
                        { this.state.error }
                    </div>
                </div>
            )
        } else if (this.state.call_id != null) {
            return(
                <div className="section">
                    <div className="is-divider" data-content="Running"></div>
                    <div className="section has-background-white-ter">
                        <p>Run with call_id: { this.state.call_id }</p>
                        {/* { this.renderLogs() } */}
                        <p> {this.state.logs} </p>
                    </div>

                </div>
            )
        } else {
            return (<div className="is-divider" data-content="Output (Empty)"></div>)
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
