package ru.viktorgezz.collector_of_all_data.config;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Getter
@Configuration
public class ValueConfiguration {

    @Value("@{services.frontend.url}")
    private String frontendUrl; 
    
    @Value("${services.python.news-processor.url}")
    private String newsProcessorUrl;

    @Value("${services.spring.candle-enricher.url}")
    private String candleEnricherUrl;

    @Value("${services.python.price-predictor.url}")
    private String pricePredictorUrl;

    @Value("${server.callback.base-url}")
    private String callbackBaseUrl;

    @Value("${server.callback.news-path}")
    private String newsCallbackPath;

    @Value("${server.callback.candle-path}")
    private String candleCallbackPath;

    @Value("${server.callback.prediction-path}")
    private String predictionCallbackPath;

    public String getNewsCallbackUrl() {
        return callbackBaseUrl + newsCallbackPath;
    }

    public String getCandleCallbackUrl() {
        return callbackBaseUrl + candleCallbackPath;
    }

    public String getPredictionCallbackUrl() {
        return callbackBaseUrl + predictionCallbackPath;
    }
}
