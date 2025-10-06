package ru.viktorgezz.collector_of_all_data.config;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final ValueConfiguration values;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Применяем ко всем путям
                .allowedOrigins(values.getFrontendUrl())
                .allowedMethods("*") // Разрешенные HTTP-методы
                .allowedHeaders("*") // Разрешить все заголовки
                .allowCredentials(true); // Разрешить отправку cookies
    }
}
