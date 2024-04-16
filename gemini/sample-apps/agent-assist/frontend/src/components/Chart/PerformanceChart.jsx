import ChartCard from "./ChartCard";

// This component is responsible for rendering a chart that shows the performance of the agent.
// The chart displays the number of policies sold and the revenue generated by the agent over time.
export default function PerformanceChart(props) {
  // The data prop contains the data that will be used to generate the chart.
  const { data } = props;

  // The x prop specifies the name of the property that will be used for the x-axis of the chart.
  const x = "months";

  // The y1 prop specifies the name of the property that will be used for the y-axis of the chart.
  const y1 = "Policies Sold";

  // The y2 prop specifies the name of the property that will be used for the secondary y-axis of the chart.
  const y2 = "Revenue";

  // The ChartCard component is responsible for rendering the chart.
  return (
    <ChartCard title="Month Wise Data" data={data} x={x} y1={y1} y2={y2} />
  );
}
