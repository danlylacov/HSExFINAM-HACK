package ru.viktorgezz.collector_of_all_data.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CombinedData {
    private String sessionId;
    private String newsData;
    private String candleData;
}
