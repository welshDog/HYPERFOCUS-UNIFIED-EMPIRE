import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from "@/components/ui/card";

interface AnalyticsChartProps {
  data: any[];
  type?: 'social' | 'engagement';
}

export function AnalyticsChart({ data, type = 'overview' }: AnalyticsChartProps) {
  const chartData = data.map(item => ({
    timestamp: new Date(item.timestamp).toLocaleDateString(),
    value: typeof item.metric_value === 'object' ? 
      item.metric_value.count || item.metric_value.value : 
      item.metric_value,
    name: item.metric_name
  }));

  return (
    <Card className="p-4">
      <h3 className="text-lg font-semibold mb-4">
        {type === 'social' ? 'Social Media Metrics' : 
         type === 'engagement' ? 'Engagement Metrics' : 
         'Overview Metrics'}
      </h3>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis />
            <Tooltip />
            <Area 
              type="monotone" 
              dataKey="value" 
              name="Value"
              stroke="#8884d8" 
              fill="#8884d8" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}