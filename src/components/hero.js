import React from 'react';


class Hero extends React.Component {
    render() {
        return (
            <section className="hero is-primary">
                <div className="hero-body">
                    <div className="container">
                        <h1 className="title">
                            { this.props.module }
                        </h1>
                        <h2 className="subtitle">
                            by PyBlitzUI
                        </h2>
                    </div>
                </div>
            </section>
        );
    }
}

export default Hero
