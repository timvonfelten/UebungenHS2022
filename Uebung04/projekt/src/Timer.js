import React, {Component} from 'react';
class Timer extends Component {

    constructor(props) {
        super(props);
        this.id = 0
        this.time = this.props.countdown
        this.state = {count:this.props.countdown}
        this.start = this.start.bind(this);
        this.counter = this.counter.bind(this);
    }

    counter(time,id)
    {
        // Timer funktion
        time -= 1;
            if (id !== this.id){
                return
            }
            if (time > 0){
                setTimeout(this.counter,1000,time,id);
            }
            if (time < 1){
                time = "FERTIG";
            }
            this.setState({count:this.state.count = time});
            return time;
    }

    start(){
        this.id += 1
        this.counter(this.time,this.id);
    }

    render() {
        return(<>
        {this.state.count} <br></br>
        <p>
        <button onClick={this.start}>(Reh)-Start</button>
        </p>
        </>)
    }
}

export default Timer;