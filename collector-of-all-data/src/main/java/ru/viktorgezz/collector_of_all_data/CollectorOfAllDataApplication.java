package ru.viktorgezz.collector_of_all_data;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class CollectorOfAllDataApplication {

	public static void main(String[] args) {
		SpringApplication.run(CollectorOfAllDataApplication.class, args);
	}

}
