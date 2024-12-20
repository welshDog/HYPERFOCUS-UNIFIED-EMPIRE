import { supabase } from "@/integrations/supabase/client";

export type AnalyticsMetric = {
  platform: string;
  name: string;
  value: any;
  source: string;
};

export async function trackAnalytics(metric: AnalyticsMetric) {
  console.log("Tracking analytics:", metric);
  const { error } = await supabase.from("analytics_data").insert({
    platform: metric.platform,
    metric_name: metric.name,
    metric_value: metric.value,
    source: metric.source,
  });

  if (error) {
    console.error("Error tracking analytics:", error);
    throw error;
  }
}

export async function fetchAnalytics(platform?: string) {
  console.log("Fetching analytics for platform:", platform);
  let query = supabase
    .from("analytics_data")
    .select("*")
    .order("timestamp", { ascending: false });

  if (platform) {
    query = query.eq("platform", platform);
  }

  const { data, error } = await query;

  if (error) {
    console.error("Error fetching analytics:", error);
    throw error;
  }

  // Add some sample data if no data exists
  if (!data || data.length === 0) {
    const sampleData = [
      {
        platform: "web",
        metric_name: "Page Views",
        metric_value: { count: 150 },
        timestamp: new Date().toISOString(),
        source: "application"
      },
      {
        platform: "social",
        metric_name: "Social Shares",
        metric_value: { count: 45 },
        timestamp: new Date().toISOString(),
        source: "twitter"
      },
      {
        platform: "web",
        metric_name: "Engagement Rate",
        metric_value: { value: 0.67 },
        timestamp: new Date().toISOString(),
        source: "application"
      }
    ];
    return sampleData;
  }

  return data;
}