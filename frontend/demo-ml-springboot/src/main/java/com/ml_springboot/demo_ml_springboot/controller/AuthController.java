package com.ml_springboot.demo_ml_springboot.controller;

import java.security.Principal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.ml_springboot.demo_ml_springboot.entity.User;
import com.ml_springboot.demo_ml_springboot.repository.UserRepository;
import com.ml_springboot.demo_ml_springboot.service.UserService;

@Controller
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/register")
    public String showRegisterForm(Model model) {
        model.addAttribute("user", new User());
        return "register";
    }

    @PostMapping("/register")
    public String registerUser(@ModelAttribute User user) {
        userService.registerUser(user);
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String showLogin(Model model, @RequestParam(value = "error", required = false) String error) {
        if (error != null) {
            model.addAttribute("errorMessage", "Invalid email or password");
        }
        return "login";
    }


    @GetMapping("/home")
    public String homePage(Principal principal,Model model) {
        String userName = userRepository.findByEmail(principal.getName()).get().getName();

        model.addAttribute("name", userName);
        return "index"; // Your existing Q&A page
    }


}

