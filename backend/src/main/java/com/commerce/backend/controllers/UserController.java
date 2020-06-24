package com.commerce.backend.controllers;

import com.commerce.backend.forms.EmailResetForm;
import com.commerce.backend.forms.PasswordResetForm;
import com.commerce.backend.domain.User;
import com.commerce.backend.services.TokenService;
import com.commerce.backend.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.security.Principal;

@RestController
public class UserController extends SecuredApiController {


    private final TokenService tokenService;
    private final UserService userService;


    @Autowired
    public UserController(TokenService tokenService, UserService userService) {
        this.tokenService = tokenService;
        this.userService = userService;

    }


    @RequestMapping(value = "/account", method = RequestMethod.GET)
    public ResponseEntity getUser(Principal principal) {
        System.out.println("GET USER");
        User user = userService.getUser(principal);
        return new ResponseEntity<User>(user, HttpStatus.OK);
    }

    @RequestMapping(value = "/account", method = RequestMethod.PUT)
    public ResponseEntity updateUser(@RequestBody @Valid User user, BindingResult bindingResult, Principal principal) {
        if (bindingResult.hasErrors()) {
            return new ResponseEntity(HttpStatus.BAD_REQUEST);
        }
        User dbUser = userService.updateUser(principal, user);
        //TODO check if there is a password leak
        return new ResponseEntity<User>(dbUser, HttpStatus.OK);
    }

    @RequestMapping(value = "/account/email/reset", method = RequestMethod.POST)
    public ResponseEntity emailReset(@RequestBody @Valid EmailResetForm emailResetForm, BindingResult bindingResult, Principal principal, HttpServletRequest request) {
        if (bindingResult.hasErrors()) {
            return new ResponseEntity(HttpStatus.BAD_REQUEST);
        }
        String appUrl = request.getRemoteHost();
        String appPort = String.valueOf(request.getServerPort());
        if (!appPort.trim().equals("")) {
            appUrl = appUrl + ":" + appPort;
        }
        tokenService.createEmailResetToken(principal, emailResetForm, appUrl);
        return new ResponseEntity(HttpStatus.OK);

    }

    @RequestMapping(value = "/account/password/reset", method = RequestMethod.POST)
    public ResponseEntity passwordReset(@RequestBody @Valid PasswordResetForm passwordResetForm, BindingResult bindingResult, Principal principal, HttpServletRequest request) {
        if (bindingResult.hasErrors()) {
            return new ResponseEntity(HttpStatus.BAD_REQUEST);
        }
        userService.resetPassword(principal, passwordResetForm);
        return new ResponseEntity(HttpStatus.OK);

    }

    @RequestMapping(value = "/account/status", method = RequestMethod.GET)
    public ResponseEntity getVerificationStatus(Principal principal) {
        Boolean status = userService.getVerificationStatus(principal);
        return new ResponseEntity<Boolean>(status, HttpStatus.OK);
    }


}
