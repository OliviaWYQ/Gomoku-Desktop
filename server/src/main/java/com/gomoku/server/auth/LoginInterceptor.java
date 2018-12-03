package com.gomoku.server.auth;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Method;
import java.util.HashMap;

@Aspect
@Component
public class LoginInterceptor {

    static private HashMap<String, String> userInfo = new HashMap<>();

    public void userLogIn(String userName, String token){
        userInfo.put(userName, token);
    }

    @Pointcut("@annotation(com.gomoku.server.auth.LoginRequired)")
    public void controllerMethodPointcut() {
    }

    @Around("controllerMethodPointcut()")
    public Object Interceptor(ProceedingJoinPoint pjp) {
        MethodSignature signature = (MethodSignature) pjp.getSignature();
        Method method = signature.getMethod();

        RequestAttributes ra = RequestContextHolder.getRequestAttributes();
        ServletRequestAttributes sra = (ServletRequestAttributes) ra;
        HttpServletRequest request = sra.getRequest();

        Object result = null;

        if (isLoginRequired(method)) {
            result = isLogin(request);
        }
        if (result == null) {
            try {
                result = pjp.proceed();
            } catch (Throwable throwable) {
                throwable.printStackTrace();
                result = "Auth problem.";
            }
        }
        return result;
    }

    private boolean isLoginRequired(Method method) {
        boolean result = false;
        if (method.isAnnotationPresent(LoginRequired.class)) {
            result = method.getAnnotation(LoginRequired.class).loginRequired();
        }
        return result;
    }

    private Object isLogin(HttpServletRequest request) {
        String token = request.getHeader("TOKEN");
        String userName = request.getHeader("USER_NAME");
        if(token==null ||userName==null || !userInfo.containsKey(userName) || !token.equals(userInfo.get(userName))){
            return "Unauthorized or timeout.";
        }
        return null;
    }

}
