import GameBoard from "../game_board/gameBoard";
import useWebSocket from "react-use-websocket";
import { useEffect } from "react";

const WebSocket = ({ id, state, handleChangeState }) => {
    const { lastJsonMessage } = useWebSocket(`ws://localhost:8000/game/${id}`)

    useEffect(() => {
        console.log(lastJsonMessage);
        handleChangeState(lastJsonMessage)
    }, [lastJsonMessage])

    return(
        <>
        <GameBoard id={id} state={state} handleChangeState={handleChangeState} />
        </>
    )
}

export default WebSocket