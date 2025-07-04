package com.ml_springboot.demo_ml_springboot.controller;

import com.ml_springboot.demo_ml_springboot.model.QAResponse;
import com.ml_springboot.demo_ml_springboot.service.RagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Controller
public class RagController {

    @Autowired
    private RagService ragService;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @PostMapping("/ask")
    public String ask(@RequestParam("file") MultipartFile file,
                      @RequestParam("question") String question,
                      Model model) throws IOException {

        String sessionId = "user-session-001"; // For now, static. Can use UUID later.

        QAResponse response = ragService.askQuestion(file, question, sessionId);

        model.addAttribute("query", response.getQuery());
        model.addAttribute("answer", response.getAnswer());
        model.addAttribute("documentId", response.getDocumentId());

        return "index";
    }
}
