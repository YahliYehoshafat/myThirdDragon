import {Line} from 'react-chartjs-2'
import {
    Chart as ChartJS, 
    CategoryScale, 
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function LineGraph({labels, pet_data, label}){
    //Creates a line chart customized according to the parameters it receives using the ChartJS library.
    const options = {
        responsive: false,
        maintainAspectRatio: false,
        layout: { padding: 0 }, 
        scales: {
            x: {
            ticks: {
                autoSkip: true,  
                maxRotation: 45, 
                minRotation: 0
            },
            grid: { offset: false } 
            },
            y: {
            beginAtZero: true
            }
        }
    };

    const data = {
        labels: labels,
        datasets: [{
            label: label,
            data: pet_data,
            borderColor: "#B0C4DE",
        }]
    };
    return(
        <>
            <Line options={options} data={data} width={550} height={250}/>
        </>
    )
}

export default LineGraph