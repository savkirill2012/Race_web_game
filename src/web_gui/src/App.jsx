import { useState, useEffect} from 'react'
import serverApi from './services/api'
import WebSocket from './components/websoket/websocket'


const App = () => {
  const [id, setId] = useState('') 
  
  useEffect(() => {
    serverApi.getPersonalId().then(response => {
      // console.log(response.id);
      setId(response.id)
    })
  }, [])

  const [ state, setState] = useState('')

  const handleChangeState = (state) => {
    // console.log('Update state from player');
    setState(state)
  } 

  if (id) {
    return (
      <>
      <WebSocket id={id} state={state} handleChangeState={handleChangeState}/>
      </>
    )
  }
}

export default App
