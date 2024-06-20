import RowBoard  from "./rowBoard"
import { useEffect } from "react"
import useWebSocket from 'react-use-websocket'
import './gameBoard.css'


var affortable_keys = ['1', '2', '3']
var special_keys = ['a', 'd', 'w', 's', 'A', 'D', 'W', 'S', 'ц', 'ф', 'в', 'ы', 'Ц', 'Ф', 'В', 'Ы', ' ']

const GameBoard = ({id, state, handleChangeState}) => {
    const { sendJsonMessage, lastJsonMessage } = useWebSocket(`ws://localhost:8000/player/${id}`)

    // const [ buttonPushed, setButtonPushed ] = useState('') 

    useEffect(() => {
        var keys = {
            a: () => sendJsonMessage({key: 4}), 
            d: () => sendJsonMessage({key: 5}),
            w: () => sendJsonMessage({key: 6}), 
            s: () => sendJsonMessage({key: 7}),
            A: () => sendJsonMessage({key: 4}), 
            D: () => sendJsonMessage({key: 5}),
            W: () => sendJsonMessage({key: 6}), 
            S: () => sendJsonMessage({key: 7}),
            ф: () => sendJsonMessage({key: 4}), 
            в: () => sendJsonMessage({key: 5}),
            ц: () => sendJsonMessage({key: 6}), 
            ы: () => sendJsonMessage({key: 7}),
            Ф: () => sendJsonMessage({key: 4}), 
            В: () => sendJsonMessage({key: 5}),
            Ц: () => sendJsonMessage({key: 6}), 
            Ы: () => sendJsonMessage({key: 7}),
            ' ': () => sendJsonMessage({key: 2})
        }
        var timers = {}
        
        document.onkeydown= function(e) {
            var key = e.key.toString()
            console.log(key);
            
            if (!(key in keys) && affortable_keys.includes(key)) {
                sendJsonMessage({key: key})
                return true;
            }
            
            if (special_keys.includes(key)) {
                if (!(key in timers)) {
                    timers[key] = null;
                    keys[key]();
                    timers[key]= setInterval(keys[key], 100);
                }
            }
            return false;
        };

        document.onkeyup= function(e) {
            var key= e.key;
            if (key in timers) {
                if (timers[key]!==null)
                    clearInterval(timers[key]);
                delete timers[key];
            }
        };
    }, [])

    useEffect(() => {
        handleChangeState(lastJsonMessage)
    }, [lastJsonMessage])


    if (state) {
        return (
            <>
            <table className="gameboard">
                <tbody>
                    {state.field.map((row) => <RowBoard row={row} />)}
                </tbody>
            </table>
            <h1>Score:</h1>
            <p className="font">{state.score}</p>
            <h1>Best score:</h1>
            <p className="font">{state.higthScore}</p>
            <p>Gamestatus</p>
            <p>{state.pause ? 'is paused' : 'play'}</p>
            <p>Use WASD to move. <br></br> Use 1 - start, 2 or space - pause, 3 - restart</p>
            </>
        )
    }

}

export default GameBoard