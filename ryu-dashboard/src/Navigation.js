import { Link } from "react-router-dom";


function Navigation(){
    return (
        <nav>
            <Link to="/"> 首頁 </Link>
            <Link to="/dashboard"> 圖表頁 </Link>
        </nav>
    )
}

export default Navigation