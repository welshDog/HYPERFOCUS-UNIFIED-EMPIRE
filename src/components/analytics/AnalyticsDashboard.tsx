import { useQuery } from "@tanstack/react-query";
import { fetchAnalytics } from "@/utils/analytics";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AnalyticsChart } from "./AnalyticsChart";
import { AnalyticsMetrics } from "./AnalyticsMetrics";

export function AnalyticsDashboard() {
  const { data: analyticsData, isLoading } = useQuery({
    queryKey: ["analytics"],
    queryFn: () => fetchAnalytics(),
  });

  if (isLoading) {
    return <div>Loading analytics...</div>;
  }

  return (
    <div className="space-y-4 p-4">
      <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
      
      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="social">Social Media</TabsTrigger>
          <TabsTrigger value="engagement">Engagement</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="p-4">
              <AnalyticsChart data={analyticsData || []} />
            </Card>
            <Card className="p-4">
              <AnalyticsMetrics data={analyticsData || []} />
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="social">
          <Card className="p-4">
            <AnalyticsChart 
              data={analyticsData?.filter(d => d.platform === 'social') || []}
              type="social"
            />
          </Card>
        </TabsContent>

        <TabsContent value="engagement">
          <Card className="p-4">
            <AnalyticsMetrics 
              data={analyticsData?.filter(d => d.metric_name.includes('engagement')) || []}
              type="engagement"
            />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}