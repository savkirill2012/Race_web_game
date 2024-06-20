import './rowBoard.css'

const RowBoard = ({row}) => {
    return (
        <tr>
            {row.map((cell) => {
                if (cell == 0) {
                    return <td className="cell-off"></td>
                } else {
                    return <td className="cell-on"></td>
                }
            })}            
        </tr>
    )
}

export default RowBoard