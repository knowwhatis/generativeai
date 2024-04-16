import ChartCard from "./ChartCard";

// This component displays a chart that shows the sales generated by different social media platforms.
export default function MarketingChart(props) {
  // The data for the chart is passed in as a prop.
  const { data } = props;

  // The x-axis of the chart shows the social media platforms.
  const x = "Social Media Platforms";

  // The y-axis of the chart shows the sales generated.
  const y1 = "Sales Generated";

  // The ChartCard component is used to display the chart.
  return (
    <ChartCard
      // The title of the chart is "Social Media Marketing Sales".
      title="Social Media Marketing Sales"
      // The data for the chart is passed in as a prop.
      data={data}
      // The x-axis of the chart shows the social media platforms.
      x={x}
      // The y-axis of the chart shows the sales generated.
      y1={y1}
    />
  );
}
