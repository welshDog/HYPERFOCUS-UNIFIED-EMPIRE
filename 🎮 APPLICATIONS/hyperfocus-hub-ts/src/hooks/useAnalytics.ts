import { trackAnalytics, AnalyticsMetric } from "@/utils/analytics";

export function useAnalytics() {
  const trackEvent = async (metric: Omit<AnalyticsMetric, "timestamp">) => {
    try {
      await trackAnalytics(metric);
    } catch (error) {
      console.error("Failed to track analytics event:", error);
    }
  };

  const trackPageView = (page: string) => {
    return trackEvent({
      platform: "web",
      name: "page_view",
      value: { page },
      source: "application"
    });
  };

  const trackEngagement = (action: string, value: any = 1) => {
    return trackEvent({
      platform: "web",
      name: `engagement_${action}`,
      value: { action, value },
      source: "application"
    });
  };

  const trackSocial = (platform: string, action: string, value: any = 1) => {
    return trackEvent({
      platform: "social",
      name: `social_${action}`,
      value: { platform, action, value },
      source: platform
    });
  };

  return {
    trackEvent,
    trackPageView,
    trackEngagement,
    trackSocial
  };
}