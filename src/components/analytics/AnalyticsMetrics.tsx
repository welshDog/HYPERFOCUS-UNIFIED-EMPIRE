import { Card } from "@/components/ui/card";
import { ReactNode } from "react";

interface AnalyticsMetricsProps {
  data: any[];
  type?: 'social' | 'engagement' | 'overview';
}

export function AnalyticsMetrics({ data, type = 'overview' }: AnalyticsMetricsProps) {
  const metrics = data.reduce((acc: Record<string, number>, curr) => {
    const value = typeof curr.metric_value === 'object' ? 
      curr.metric_value.count || curr.metric_value.value : 
      curr.metric_value;
    
    if (!acc[curr.metric_name]) {
      acc[curr.metric_name] = 0;
    }
    acc[curr.metric_name] += value;
    return acc;
  }, {});

  return (
    <Card className="p-4">
      <h3 className="text-lg font-semibold mb-4">
        {type === 'social' ? 'Social Media Summary' : 
         type === 'engagement' ? 'Engagement Summary' : 
         'Metrics Summary'}
      </h3>
      <div className="grid gap-4 md:grid-cols-2">
        {Object.entries(metrics).map(([name, value]) => (
          <Card key={name} className="p-4">
            <h4 className="text-sm font-medium text-gray-500">{name}</h4>
            <p className="text-2xl font-bold">{String(value)}</p>
          </Card>
        ))}
      </div>
    </Card>
  );
}