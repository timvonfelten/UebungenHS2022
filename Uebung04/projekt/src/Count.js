import React, {Component} from 'react';

class Count extends Component {
    constructor(props) {
        super(props);

    this.state = {count:0}
    this.increase = this.increase.bind(this)
    }

    increase(){
        this.setState({count:this.state.count + 1});
    }

    render() {
        return(<>
        {this.state.count} <br></br>
        <button onClick={this.increase}>Kligg</button>
        </>)
    }


}

export default Count;