import "./home.css";
import { useNavigate } from "react-router-dom";


function Home() {
    const navigate = useNavigate();

  const handleCustomSheetsClick = () => {
    navigate("/custom-sheets");
  }

  const handleScanSheetsClick = () => {
    navigate("/scan-sheets");
  }

  
  return (
    <>
      <div className="homeContainer">
        <div className="title">Bubble Scan</div>
        <div className="subtitle">Grading Made Easy</div>
        <div className="buttons">
          <button className="button button-scan" onClick={handleScanSheetsClick}>Scan</button>
          <button className="button button-custom" onClick={handleCustomSheetsClick} >Custom Sheets</button>
        </div>
        </div>

        <div className="homeContent">
          <h3>Bubble Scan</h3>
          <p>
            Lorem ipsum odor amet, consectetuer adipiscing elit. Ultrices ex
            adipiscing mauris posuere quis felis. Consectetur posuere lobortis
            primis est sagittis. Ultrices gravida penatibus magnis primis
            rhoncus per varius nisl. Congue malesuada integer euismod dignissim
            purus. Ad velit fermentum vulputate gravida aptent. Morbi est tempus
            efficitur turpis blandit rutrum. In nulla nullam phasellus convallis
            ut natoque metus. Ex placerat nunc iaculis consectetur vehicula
            pharetra porttitor. Integer potenti massa tortor luctus pellentesque
            pellentesque litora aliquet egestas.
          </p>
        </div>
      
    </>
  );
}

export default Home;
