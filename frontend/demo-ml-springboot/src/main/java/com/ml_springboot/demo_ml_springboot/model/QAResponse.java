package com.ml_springboot.demo_ml_springboot.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class QAResponse {
    private String query;
    private String answer;
    private String documentId;


    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }
}
