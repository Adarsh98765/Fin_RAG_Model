package com.ml_springboot.demo_ml_springboot.service;

import com.ml_springboot.demo_ml_springboot.model.QAResponse;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@Service
public class RagService {

    @SuppressWarnings("null")
    public QAResponse askQuestion(MultipartFile file, String question, String sessionId) throws IOException {
        String url = "http://localhost:8003/ask";  // Model_3 FastAPI endpoint

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        ByteArrayResource resource = new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();
            }
        };

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("pdf", resource);
        body.add("question", question);
        body.add("session_id", sessionId); // ✅ Required by updated Model_3

        HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(body, headers);

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<Map> response = restTemplate.postForEntity(url, request, Map.class);

        QAResponse qa = new QAResponse();
        qa.setQuery(question);
        qa.setAnswer((String) response.getBody().get("answer"));
        qa.setDocumentId((String) response.getBody().get("document_id"));
        return qa;
    }
}
