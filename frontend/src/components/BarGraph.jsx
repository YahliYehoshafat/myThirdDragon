import {Bar} from 'react-chartjs-2'
import {
    Chart as ChartJS, 
    CategoryScale, 
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

function BarGraph({labels, pet_data, label}){
    //Creates a bar chart customized according to the parameters it receives using the ChartJS library.
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
            borderWidth: 1,
        },],
    };
    return(
        <>
            <Bar options={options} data={data} width={550} height={250}/>
        </>
    )
}

export default BarGraph