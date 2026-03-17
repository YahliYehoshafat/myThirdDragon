import ProgressBar from 'react-bootstrap/ProgressBar';

function MyProgressBar({ value, label }) {
  //A progress bar that allows you to see the properties status in a visually appealing and eye-friendly way.
  return (
    <ProgressBar 
      now={value} 
      label={`${label}: ${value}%`} 
      style={{ width: '900px', height: "20px", marginLeft: "300px", marginTop: "100px", marginBottom: "100px" }} 
    />
  );
}

export default MyProgressBar;