import axios from "axios"

const baseUrl = 'http://localhost:8000'


const getPersonalId = () => {
    return axios.get(`${baseUrl}/id`).then((response => {
        console.log(response);
        return response.data}))
}



export default {getPersonalId}