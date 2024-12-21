import { useQuery } from "@tanstack/react-query";
import { fetchAnalytics } from "@/utils/analytics";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AnalyticsChart } from "./AnalyticsChart";
import { AnalyticsMetrics } from "./AnalyticsMetrics";

const AnalyticsDashboard = () => {
  const { data: analyticsData, isLoading, error } = useQuery({
    queryKey: ["analytics"],
    queryFn: () => fetchAnalytics(),
  });

  console.log("Analytics data:", analyticsData); // Debug log

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-red-500">Error loading analytics data</div>
      </div>
    );
  }

  if (!analyticsData || analyticsData.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">No analytics data available</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">      
      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="social">Social Media</TabsTrigger>
          <TabsTrigger value="engagement">Engagement</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="p-4">
              <AnalyticsChart data={analyticsData} type="overview" />
            </Card>
            <Card className="p-4">
              <AnalyticsMetrics data={analyticsData} type="overview" />
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="social" className="mt-4">
          <Card className="p-4">
            <AnalyticsChart 
              data={analyticsData.filter(d => d.platform === 'social') || []}
              type="social"
            />
          </Card>
        </TabsContent>

        <TabsContent value="engagement" className="mt-4">
          <Card className="p-4">
            <AnalyticsMetrics 
              data={analyticsData.filter(d => d.metric_name.includes('engagement')) || []}
              type="engagement"
            />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

AnalyticsDashboard.displayName = "AnalyticsDashboard";

export default AnalyticsDashboard;